# This program is designed to port scan an entire network.  It was specifically designed for the output from the
# arp -a command to be copy/pasted into the input file, although it should be able to sort through most text and discern the ipv4
# addresses to be scanned.  Any ipv4 address entered in the input file will be scanned from ports 1-2000 and the open ports will be printed.
import socket
import threading
from queue import Queue
import re


q = Queue()

# process_info is the function that takes the arp -a output and processes it so it can be used by the scanner function.
# it takes one input variable, filename (a sting), specified in the scanner function definition as 'input.txt', although this can
# be changed.  It outputs a list of all device ipv4 addresses in the input file, which it passes to scanner to be scanned.
def process_info(filename):
    a = []
    str1 = ""

    with open(filename, 'rt') as file:
        for line in file:
            a.append(line)

    for element in a:
        str1 += element

    ips = re.findall(r'([1-9]+\.[1-9]+\.[1-9]+\.[1-9]+)', str1)
    return ips

# scanner is the function that does the actual port scanning.  It takes one input variable, port (an integer), which it gets from the queue
# (specified in the threader function).  If a port is open it will output the port and the device ip, if not it will do nothing.
def scanner(port, filename='input.txt'):
    addresses = process_info(filename)
    lock = threading.Lock()
    for address in addresses:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex((address, port))
        s.close()
        with lock:
            if result == 0:
                print("Port ", port, " is open on", address)
            else:
                pass

# threader is the function that allows the threads to function. Each thread retrieves and removes a number from the queue
# and passes it to scanner.  There are no input variables
def threader():
    while True:
        number = q.get()
        scanner(number)
        q.task_done()

# puts numbers in a specified range into a queue to be used as port numbers by the threads; this range will determine what
# ports are scanned
for port in range(1, 2000):
    q.put(port)

# initializes 10 threads (could be more/less) and tells them to run threader
for thread in range(10):
    t = threading.Thread(target=threader)
    t.start()
