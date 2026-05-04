# Send NTCIP 1202 using UDP
import socket, sys
from binascii import unhexlify
from time import sleep

IP = '127.0.0.1'
PORT = '6053'

def main():
    # send payload to IP + PORT
    sk = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    # open and read from file, then close file
    f = open('fixedFull.txt', 'r') # change to pcapOutput.txt for initial TSC pcap extraction
    Lines = f.readlines()
    f.close()

    print('Sending.\nPress Ctrl+C to exit')
    sleep(1)
    try:
        while(1):
            for line in Lines:
                data = line.strip('\n')
                #print(data)                        # uncomment to view stream
                # send Hex string to port
                unhexed = unhexlify(data)
                sk.sendto(unhexed,(IP,int(PORT)))
                sleep(0.1)              # 0.1 for NTCIP 1202
    except KeyboardInterrupt:
        print('\nStopping tscScript.')
    finally:
        sk.close()

if __name__=="__main__":
    sys.exit(main())
