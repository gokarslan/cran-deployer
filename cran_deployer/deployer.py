#!/usr/bin/env python3

import argparse
import os
import subprocess
import sys

from colorama import init
from termcolor import cprint
from pyfiglet import figlet_format
import yaml

from cran_deployer.log import LOG
from cran_deployer.log import setup as log_setup


def create_hosts_file(config, playbook_path):
    data = ""
    try:
        pod = config["pod"]
        data += "[controller]\n"
        for control in pod["controller"]:
            host_name = list(control.keys())[0]
            data += host_name + " ansible_host=" + control[host_name]["host_ip"] + "\n"
        data += "\n[compute]\n"
        for compute in pod["compute"]:
            host_name = list(compute.keys())[0]
            data += host_name + " ansible_host=" + compute[host_name]["host_ip"] + "\n"
    except KeyError:
        LOG.error("An error has occured while reading the pod information from the config file.")
        sys.exit(-1)
    with open(playbook_path + "/hosts", "w") as f:
        f.write(data)


def create_group_vars(config, playbook_path):
    with open(playbook_path + "/group_vars/all.yaml", 'w') as f:
        yaml.dump(config, f, default_flow_style=False)


def main():
    init(strip=not sys.stdout.isatty())
    cprint(figlet_format('BoUn CRAN', font='speed'), 'blue')  # attrs=['bold']
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', "--install", dest='install',
                        action='store_true',
                        default=False,
                        help='install Devstack')
    parser.add_argument('-u', "--uninstall", dest='uninstall',
                        action='store_true',
                        default=False,
                        help='uninstall Devstack')
    parser.add_argument('-p', "--post-install", dest='post_install',
                        action='store_true',
                        default=False,
                        help='runs post install scripts')
    parser.add_argument('-y', action="store_true", dest="y", default=False,
                        help="answer yes to all prompts")
    parser.add_argument('-c', '--config-file', dest="config_file",
                        default="cran_deployer/config.yaml",
                        help="path for configuration file")
    parser.add_argument('--playbook-path', dest="playbook_path",
                        default=os.path.dirname(os.path.abspath(__file__)) + "/playbooks",
                        help="path for the playbooks")
    parser.add_argument("--no-retry", action="store_true", dest="no_retry", default=False,
                        help="if given, playbooks will run from scratch")
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s {version}'.format(version="0.0.5"))
    parser.add_argument("--debug", action="store_true", dest="debug", default=False,
                        help="set log level to debug")

    opts, _ = parser.parse_known_args()

    log_setup(debug=opts.debug)

    # Read configuration
    config = None
    with open(opts.config_file, 'r') as f:
        config = yaml.load(f)
    if not config:
        LOG.error("Incorrect config file at %s", opts.config_file)
        return -1

    ansible_command = "ansible-playbook -i " + opts.playbook_path + "/hosts"

    if opts.install:
        # TODO: run some test first
        if opts.y or 'y' in input("Do you want to install devstack? [Y/n] ").lower():
            create_hosts_file(config=config, playbook_path=opts.playbook_path)
            create_group_vars(config=config, playbook_path=opts.playbook_path)
            process_cmd = ansible_command + " " + opts.playbook_path + "/install.yaml"
            if 'network_configure' in config and not config['network_configure']:
                process_cmd += ' --skip-tags "network_configure"'
            if not opts.no_retry and os.path.isfile(opts.playbook_path + "/install.retry"):
                process_cmd += " --limit @" + opts.playbook_path + "/install.retry"
            LOG.info("Executing: %s", process_cmd)
            process = subprocess.Popen(process_cmd.split(), stdout=subprocess.PIPE)
            for line in iter(process.stdout.readline, b''):
                print(line.decode("utf-8")[:-1])
    # Post installation scripts builds vms and do a simple ping test
    if opts.post_install:
        process_cmd = ansible_command + " " + opts.playbook_path + "/post_install.yaml"
        if not opts.no_retry and os.path.isfile(opts.playbook_path + "/post_install.retry"):
            process_cmd += " --limit @" + opts.playbook_path + "/install.retry"
        LOG.info("Executing: %s", process_cmd)
        process = subprocess.Popen(process_cmd.split(), stdout=subprocess.PIPE)
        for line in iter(process.stdout.readline, b''):
            print(line.decode("utf-8")[:-1])
    if opts.uninstall:
        if opts.y or 'y' in input("Do you want to uninstall devstack? [Y/n] ").lower():
            process_cmd = ansible_command + " " + opts.playbook_path + "/uninstall.yaml"
            if not opts.no_retry and os.path.isfile(opts.playbook_path + "/post_install.retry"):
                process_cmd += " --limit @" + opts.playbook_path + "/post_install.retry"
            process = subprocess.Popen(process_cmd.split(), stdout=subprocess.PIPE)
            for line in iter(process.stdout.readline, b''):
                print(line.decode("utf-8")[:-1])
    return 0


if __name__ == "__main__":
    sys.exit(main())
