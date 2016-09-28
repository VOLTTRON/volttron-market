# README #

This repository contains VOLTTRON agents and classes useful for creating double-auction transactive markets. Typically, the Buyer, Seller and Middleman agents would not be run on the VOLTTRON platform as provided, but instead would be installed into the VOLTTRON virtual environment and extended by agents requiring this functionality.

## INSTALLATION ##

The following instructions assume you have already cloned this repository, and that you have already installed the [PubSub](https://github.com/VOLTTRON/volttron-pubsub) modules into the VOLTTRON environment's site-packages directory.

Make sure you have installed [VOLTTRON](https://github.com/VOLTTRON/volttron) and its dependencies
Enable the VOLTTRON virtual environment
~~~
$ . [VOLTTRON repository location]/env/bin/activate
~~~
Install the package.
~~~
$ cd [volttron-market repository location]
$ python setup.py install
~~~

## PACKAGING AND RUNNING ##

TBD


