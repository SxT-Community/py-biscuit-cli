# SxT Python Biscuit CLI

Sometimes you need to quickly generate different biscuits rapidly for testing purposes. Since the release of [Biscuit Python](https://python.biscuitsec.org/) it's become a lot easier to generate Biscuits in Python. The purpose of this tool is to put a simple CLI wrapper around the Biscuit Python library that's modeled specifically for use with Space and Time. 

This is an early work in progress. Please use it with caution! 

```shell
└─[$] python py-biscuit-cli.py -h                                                                                                                                                              [15:34:15]
usage: py-biscuit-cli.py [-h] [-bpk BISCUIT_PRIVATE_KEY] -rid RESOURCE_ID

Space and Time Biscuit Python CLI Help Menu 🚀

options:
  -h, --help            show this help message and exit
  -bpk BISCUIT_PRIVATE_KEY, --biscuit-private-key BISCUIT_PRIVATE_KEY
                        Private key you want to create your biscuit with
  -rid RESOURCE_ID, --resource-id RESOURCE_ID
                        Resource ID you want to assoicate your biscuit with
```