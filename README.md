# Arpspoof-all
It's a project that i made out of boredom, but i think it's pretty cool.

Basically, you can drop all of the packets of the devices that are connected to the same internet you are connected. It finds all of the ip's of the devices connected to the internet and performs an MITM attack to all the devices at the same time and after that it interrupts their internet connection.
More features can be added to the project, because after you establish the MITM connection, you can perform a bunch of oterh cool attacks.

# Prerequisites
You need an wireless adapter in order to connect either from inside you kali machine or from your local machine.

## Installation

```console
# clone the repo
$ git clone https://github.com/stefan18-ux/Arpspoof-all/

# change the working directory to sherlock
$ cd Arpspoof-all

# install the requirements
$ python3 -m pip install -r requirements.txt
```
## Usage

```
python3 main.py
```
