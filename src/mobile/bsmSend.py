# SAE J2735 Message Sender
from threading import Thread
import socket
import binascii as ba
from time import sleep
import bsmGenerator

def send(ip_send, port_send, bsm, broadcast):
    try:
        while True:
            sk_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sk_send.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # set broadcast
            sk_send.bind((ip_send, 0))
            sk_send.sendto(bsm, (broadcast, port_send)) # broadcast message
            sk_send.close()
            sleep(0.1)
    except Exception as e:
        print(f"Error in send function: {e}")

def generate_bsm():
    # Declarations
    ip_send = '192.168.0.255'
    broadcast = '255.255.255.255'
    port_send = 26789
    
    try:
        while True:
            data = bsmGenerator.encoded_bsm
            if data is not None:
                unhexed = ba.unhexlify(data)
                # Uncomment the following line to print payload
                # print(unhexed)
                send(ip_send, port_send, unhexed, broadcast)
            sleep(0.1)
    except Exception as e:
        print(f"Error in generate_bsm function: {e}")

def main():
    print("Broadcasting messages.")
    print('Press Ctrl+C to exit.')

    generateThread = Thread(target=generate_bsm, daemon=True) 
    generateThread.start()
    print("Generate BSM Thread Started.")

    # Keeping the main thread alive to let the daemon thread run
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        print("Exiting.")

if __name__ == '__main__':
    main()
