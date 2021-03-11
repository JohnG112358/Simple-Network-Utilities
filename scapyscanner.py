# requires scapy - https://scapy.net
from scapy.layers.inet import ICMP, IP
from scapy.sendrecv import sr1


def main(start, stop, first_octets):
    """
    Iterates over a given ip range and pings all ips in the range to determine weather ot not they are live hosts

    Args:
        start: an integer specifying the start value of the ip range to be iterated over
        stop: an integer specifying the end value of the ip range to be iterated over
        first_octets: a string specifying the first three octets of the ip range you would like to iterate over

    Returns:
        prints to the console each ip in the range and weather it is online or not

    Raises:
      Scapy_Exception No /dev/bpf handle is available if not run with sudo privileges
      Scapy and Pycharm don't work together very well - make sure to pip install in an outside terminal
      (not the one built into Pycharm) in the project directory.  Additionally, Pycharm won't recognize Scapy if you import
      all of Scapy's modules, so you have to import each module or function you need individually.
    """
    for ip in range(start, stop):
        packet = IP(dst=first_octets + "." + str(ip), ttl=2) / ICMP()  # creates the packet that will be sent to each IP address
        reply = sr1(packet, timeout=2)  # sends the packet and looks for a response
        if not (reply is None):  # if there is a reply, prints the host is online, if there is no reply, prints the host is not online
            print(packet.dst, "is online")
        else:
            print(packet.dst, "is offline")


if __name__ == "__main__":
    main(0, 256, "octets go here")  # should be changed depending on your network setup
