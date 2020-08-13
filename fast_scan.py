# this is a port scanner that takes advantage of multi-threading - making it the fastest but also the most noticeable
import socket
import threading
from queue import Queue

q = Queue()
# target ip
address = socket.gethostbyname("192.168.1.32")
lock = threading.Lock()

# scanner is a simple port scanner with 1 input variable - port. port in and integer and scanner will output weather or
# not that port is closed
def scanner(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = s.connect_ex((address, port))
    s.close()
    with lock:
        if result == 0:
            print("Port ", port, " is open")
        else:
            print("Port ", port, " is closed")


# puts numbers in a specified range into a queue to be used as port #s by the threads; this range will determine what
# ports are scanned
for port in range(1, 60000):
    q.put(port)

# threader is the function that allows the threads to function. each thread retrieves and removes a number from the queue
# and passes it to scanner.  There are no input variables
def threader():
    while True:
        number = q.get()
        scanner(number)
        q.task_done()


# initializes 10 threads (could be more/less) and tells them to run threader
for thread in range(10):
    t = threading.Thread(target=threader)
    t.start()
