# this is the slowest port scanner but it is also the most stealthy
import socket
import time
import random

# target ip
address = socket.gethostbyname("192.168.1.32")
a = []


# random choice takes 2 input variables, start and stop, both of which are integers. It will output a random number in the
# range between start and stop while never repeating a number.
def random_choice(start, stop):
    if a == []:
        for number in range(start, stop):
            a.append(number)
    choice = random.choice(a)
    a.remove(choice)
    return choice

# scanner is the simple port scanner modified to scan port numbers randomly (as opposed to linearly) and wait a random amount
# of time in between scans.  scanner takes 2 input variables, start and stop, both of which are integers, and represent the
# bounds of the range of port numbers to be scanned.  scanner will output each port number in the range with a statement
# saying weather or not they are closed.
def scanner(start, stop):
    while True:
        port = random_choice(start, stop)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex((address, port))
        s.close()
        if result == 0:
            print("Port ", port, " is open")
        else:
            print("Port ", port, " is closed")
        time.sleep(random.randint(1, 10))
        if a == []:
            break


scanner(1, 25)
