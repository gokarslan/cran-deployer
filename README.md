# CloudRAN Deployer

CRAN Deployer is an OpenStack installation tool for CRAN testbeds. It uses the Devstack installer 
and deploys OpenStack with OvS, ODL, and Ceph as distributed storage backend.

## Supported Pods

The current version of CRAN Deployer supports two types of nodes in a pod:
1. A **control** node: *ceph needs to be installed on the control node*
2. Multiple **compute** nodes

## Installation

CRAN deployer requires python3, and the required packages can be installed using

```pip3 install -r requirements.txt ```

CRAN deployer can be run from any computer having ansible and ssh access to all nodes of the pod. 
Once the configuration file is updated (`config.yaml` is the default path) and the hosts file is updated
it can be run using

``` ./cran-deployer.py -i -p```

One simple trick is to update `/etc/hosts` file of the host computer so that `hosts` file can contain
only the names of the nodes.
