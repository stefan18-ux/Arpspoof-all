# Arpspoof-all

**Arpspoof-all** is a network security tool designed to perform Man-In-The-Middle (MITM) attacks on all devices connected to the same local network. Once the tool discovers the IP addresses of the connected devices, it simultaneously launches MITM attacks and can interrupt their internet connections. 

The tool is designed with extensibility in mind, meaning that after establishing the MITM connection, you can further implement and execute a variety of additional network attacks.

## Prerequisites

To run **Arpspoof-all**, you'll need the following:

- A wireless adapter to interact with network traffic. This can be either from within a Kali Linux machine or from your local machine.
- Basic Python dependencies and development libraries for packet manipulation.

## Installation

To install and set up the project, follow these steps:

```bash
# Clone the repository
$ git clone https://github.com/stefan18-ux/Arpspoof-all/

# Change the working directory to the project folder
$ cd Arpspoof-all

# Install the required dependencies
$ sudo apt-get install build-essential libnfnetlink-dev libnetfilter-queue-dev
$ sudo pip install netfilterqueue
```

## Usage

To run the tool, execute the following command:

```bash
$ python3 main.py
```

Note: It is recommended to run the tool for approximately 10 seconds initially, and then run it again. The accuracy of the netdiscover command used for identifying connected devices may improve after the first execution.

