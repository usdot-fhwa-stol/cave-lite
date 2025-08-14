## Receive, Decode, Broadcast SAE J2735 Messages
import os, os.path
import sys, socket
import datetime
import time
from binascii import unhexlify
from threading import Thread, Event
from pathlib import Path

# Specify the project root and asn file path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
ASN_PATH = PROJECT_ROOT / "asn_j2735"

try:
    sys.path.append(ASN_PATH.as_posix())
    import J2735_202409
except ImportError as e:
    print("Error importing ASN.1 modules:", e)
    sys.exit(1)

## Uncomment below if physical digital signal head will be used
# from gpiozero import LED

## Uncomment to declare LED pins and set initial states for signal head hardware
# red = LED(17)
# yellow = LED(27)
# green = LED(22)
# red.on()
# yellow.off()
# green.off()

# Declarations
print('Starting intersect.')
IP_LISTEN = '127.0.0.1'
IP_SEND = '192.168.0.255'
BROADCAST = '255.255.255.255'
PORT_LISTEN = 1516 # listen to Immediate Forward Plugin
PORT_SEND = 5005

## uncomment all fout.* to write logs
# fout = writeLog()

def writeLog():
    path = os.getcwd() + "/logs/"
    stamp = str(datetime.datetime.now())
    timestamp = stamp.replace("-", "_")
    timestamp = timestamp.replace(" ", "_")
    timestamp = timestamp.replace(":", "")
    timestamp = timestamp.replace(".", "")
    logPath = os.path.join(path, timestamp+".log")
    fout = open(logPath, 'w')
    return fout

print("Waiting to receive data\n")


class MessageIntersect:
    """Receive, decode, and rebroadcast SAE J2735 messages."""

    # Class-level mirrors so other modules can read updatingState and countdown
    updatingState = None
    countdown = None

    def __init__(self,
                 ip_listen: str = IP_LISTEN, port_listen: int = PORT_LISTEN,
                 ip_send: str = IP_SEND, port_send: int = PORT_SEND,
                 broadcast: str = BROADCAST, message_frame = J2735_202409):
        
        self.ip_listen = ip_listen
        self.port_listen = port_listen
        self.ip_send = ip_send
        self.port_send = port_send
        self.broadcast = broadcast
        self.message_frame = message_frame

        self.msg_ids = ['0013']  # can be extended to include other J2735 PSIDs

        # Mirrors for external access
        self.updatingState = None
        self.countdown = None

        # Control
        self._stop_event = Event()
        self._thread = Thread(target=self.intersect, args=(), daemon=True)

        # Sockets
        self.sk_listen = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sk_listen.bind((self.ip_listen, self.port_listen))
        self.sk_listen.settimeout(1.0)

        self.sk_send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Bind to a local address; OS picks the port. If binding to ip_send fails, fall back.
        try:
            self.sk_send.bind((self.ip_send, 0))
        except OSError:
            self.sk_send.bind(('', 0))
        self.sk_send.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    def start(self):
        self._thread.start()

    def stop(self, timeout=None):
        self._stop_event.set()
        try:
            self._thread.join(timeout=timeout)
        except Exception:
            pass
        # Close sockets
        try:
            self.sk_listen.close()
        except Exception:
            pass
        try:
            self.sk_send.close()
        except Exception:
            pass

    def _write_phase(self, phase):
        # fout.writelines(["Phase ", str(phase), ': '])
        print("Phase ", str(phase), ': ')

    def _write_state(self, state):
        # fout.writelines([str(state),  "\n"])
        print(str(state),  "\n")
        # Mirror to class-level for external readers
        MessageIntersect.updatingState = state

    def _write_time(self, endTime, currentSec, currentDecSec):
        currentTime = currentSec + currentDecSec / 10.0
        self.countdown = round(endTime - currentTime, 2)
        # fout.writelines(["Time to next state: {:.1f}".format(self.countdown)])
        print("Time to next state: {:.1f}".format(self.countdown))
        # Mirror to class-level for external readers
        MessageIntersect.countdown = self.countdown

    def intersect(self):
        while not self._stop_event.is_set():
            try:
                pkt = self.sk_listen.recvfrom(10000)[0]
            except socket.timeout:
                continue
            except OSError:
                break

            data = str(pkt)
            data = ''.join(data.split())

            for msg_id in self.msg_ids:
                idx = data.find(msg_id)

                # extract, decode, and send message from stream
                if idx > -1:
                    # extract
                    if int('0x' + data[idx + 4], 16) == 8:
                        lenstr = int('0x' + data[idx + 5:idx + 8], 16) * 2 + 6
                    else:
                        lenstr = int('0x' + data[idx + 4:idx + 6], 16) * 2 + 6

                    if lenstr <= len(data) - idx + 1:
                        # decode
                        msg = data[idx:idx + lenstr].encode('utf-8')
                        decode = self.message_frame.MessageFrame.MessageFrame
                        decode.from_uper(unhexlify(msg))

                        frame = decode()

                        try:
                            intersection_states = frame['value'][1]['intersections'][0]['states']
                        except Exception:
                            continue

                        utcTime = time.gmtime()
                        utcMin = utcTime.tm_min
                        utcSec = utcTime.tm_sec
                        utcDeci = int((time.time() % 1) * 10)
                        currentSec = utcMin * 60 + utcSec

                        timeEndSec = None
                        for st in intersection_states:
                            currentPhase = st.get('signalGroup')
                            currentState = str(st['state-time-speed'][0]['eventState'])
                            minEndTime = st['state-time-speed'][0]['timing']['minEndTime']

                            if currentPhase == 2:  # extend to other phases as needed
                                self._write_state(currentState)
                                self._write_phase(currentPhase)
                                timeEndSec = minEndTime / 10
                                self.updatingState = currentState
                                # mirror now to class-level
                                MessageIntersect.updatingState = currentState

                        if timeEndSec is not None:
                            self._write_time(timeEndSec, currentSec, utcDeci)

                        # send
                        try:
                            self.sk_send.sendto(msg, (self.broadcast, self.port_send))
                        except Exception:
                            # Don't crash on send errors; continue loop
                            pass


# Run the intersect in a background thread
try:
    intersect = MessageIntersect()
    intersect.start()
except Exception:
    print("Starting thread did not work")

# Convenience accessors for external modules
def get_updating_state():
    """Return the latest event state string (e.g., 'stop-And-Remain')."""
    return MessageIntersect.updatingState


def get_countdown():
    """Return the latest countdown."""
    return MessageIntersect.countdown
