# SAE J2735 Message Sender
from threading import Thread
import socket, sys
import binascii as ba
from time import sleep
import bsmGenerator


def send(ip_send, port_send, bsm, broadcast):
    sk_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sk_send.bind((ip_send, 0))
    sk_send.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # set broadcast
    sk_send.sendto(bsm, (broadcast, port_send)) # broadcast message
    sk_send.close()

def generate_bsm():
    global unhexed
    while(1):
        data = bsmGenerator.encoded_bsm
        unhexed = ba.unhexlify(data)
        # uncomment following line to print payload
        # print(unhexed)
        sleep(0.1)
    
def main():
    # Declarations
    ip_send = '192.168.0.255'
    broadcast = '255.255.255.255'
    port_send = 26789

    print("Broadcasting messages.")
    print('Press Ctrl+C to exit.')

    generateThread = Thread(target = generate_bsm, args=(),  daemon = True) 
    generateThread.start()
    print("Generate BSM Thread Started.")

    while(1):
        send(ip_send, port_send, unhexed, broadcast)
        sleep(0.1)


if __name__ == '__main__':
  sys.exit(main())
