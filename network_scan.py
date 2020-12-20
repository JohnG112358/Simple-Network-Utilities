# keyboard error catching currently not functional
import socket
import threading
from queue import Queue
import re
import os
import sys

q = Queue()
cmd = "arp -a > input.txt"  # command that generates ips to be scanned


def process_info(filename):
    """
    Takes arp -a output and creates a list of ips from the output to be used by scanner function

    Args:
        filename: a string specifying the file to be process, defined in scanner
    Returns:
        a list of all ips within the arp -a output
    Raises:
        none
    """
    a = []
    str1 = ""

    with open(filename, 'rt') as file:
        for line in file:
            a.append(line)

    for element in a:
        str1 += element

    ips = re.findall(r'([1-9]+\.[1-9]+\.[1-9]+\.[1-9]+)', str1)  # finds ipv4 addresses in input file
    return ips


def scanner(port, filename='input.txt'):
    """
    Competes the port scan by performing a full tcp connect on a given port

    Args:
        port: an integer specifying the port to connect on
        filename: a string defining the file containing the ips to be scanned, predefined as input.txt

    Returns:
        prints any open ports and the device ips to the console

    Raises:
        none
    """
    try:
        addresses = process_info(filename)
        lock = threading.Lock()
        for address in addresses:  # iterates over addresses in list addresses, attempts to connect on port number from queue
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = s.connect_ex((address, port))
            s.close()
            with lock:  # prints results, lock prevents multiple threads printing at same time
                if result == 0:
                    print("Port ", port, " is open on", address)
                else:
                    pass
    except KeyboardInterrupt:
        print("Program Concluded")
        sys.exit()


def threader():
    """
    target function for threads, threads retrieve number from queue to act as port number and run scanner

    Args:
    none

    Returns:
        none
    Raises:
        none
    """
    while True:
        number = q.get()
        scanner(number)
        q.task_done()


def main():
    """
    main function, runs command to generate device ips, initializes queue with port numbers, initializes threads

    Args:
    none

    Returns:
        none

    Raises:
        none
    """
    os.system(cmd)

    for port in range(1, 2000):  # initializes que, numbers serve as port numbers
        q.put(port)

    for thread in range(10):  # initializes 10 threads (could be more/less) and tells them to run threader
        t = threading.Thread(target=threader)
        t.start()


if __name__ == "__main__":
    main()
