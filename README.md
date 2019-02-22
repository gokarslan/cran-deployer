[![Build Status](https://travis-ci.com/gokarslan/cran-deployer.svg?token=q3HaKjfJDzXzenoF3wmP&branch=master)](https://travis-ci.com/gokarslan/cran-deployer)
# CloudRAN Deployer

CRAN Deployer is an OpenStack installation tool for CRAN testbeds. It uses the Devstack installer 
and deploys OpenStack with OvS, ODL, and Ceph as distributed storage backend.

CRAN Deployer requires python3 and pip3.

## Supported Pods

The current version of CRAN Deployer supports two types of nodes in a pod:
1. A **control** node: *ceph needs to be installed on the control node*
2. Multiple **compute** nodes

Each node must run Ubuntu, preferably 16.04.

## Deployer installation

#### Cloning from git (Preferred for development)

Simply clone the repo from the github. CRAN deployer requires python3, and the required packages 
can be installed using

```pip install -r requirements.txt ``` 

finally, run  `./cran-deployer`

#### Pip (Preferred for production)

Install `cran_deployer-<VERSION>-py3-none-any.whl` and run

```pip install cran_deployer-<VERSION>-py3-none-any.whl```

The executable `cran-deployer` will be installed to the python library.

## CRAN Installation

CRAN deployer can be run from any computer having ansible and ssh access to all nodes of the pod. 
Once the configuration file is updated (`config.yaml` is the default path) and the hosts file is updated
it can be run using

``` cran-deployer -i -p```

## CRAN Uninstalling

If you want to uninstall everything from the pod run:


``` cran-deployer -u```


## TODO
1. Implementing a simple python script `cirros_test.py` to test connectivity between two cirros nodes
using openstack python API
2. Current playbooks does not have enough tags for skipping some of the jobs. Moreover, user might 
want to install only on some of the nodes.
3. The current way of building /etc/network/interfaces file might not be generic for all kinds of hosts.
4. **SSH KEYS NEEDS TO BE SHARED BETWEEN HOSTS BEFORE RUNNING THE SCRIPTS**