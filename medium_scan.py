# this is just a basic port scanner, optimized for neither speed nor stealth
import socket

# ip address of the target
address = socket.gethostbyname("192.168.1.32")


# scanner has 2 input variables, start and stop, which are both integers.  They represent the bounds of the range of
# port numbers to be scanned. scanner will output each port scanned in the range in a linear order (ie. 1, 2, 3, etc.)
# with a statement saying weather they are open or closed
def scanner(start, stop):
    for port in range(start, stop):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = s.connect_ex((address, port))
        s.close()
        if result == 0:
            print("Port ", port, " is open")
        else:
            print("Port ", port, " is closed")


scanner(1, 10000)
