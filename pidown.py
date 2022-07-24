#!/usr/bin/env python3
import time
from subprocess import call
from argparse import ArgumentParser
from dronekit import connect

parser = ArgumentParser(description="Pi shutdown from mav using rc option")

parser.add_argument("--baudrate", type=int,
                  help="master port baud rate", default=921600)
parser.add_argument("--connect", required=True, help="connection string")
parser.add_argument("--system", type=int, default=1, help="source system id")
parser.add_argument("--timeout", type=int, default=60, help="timeout")
args = parser.parse_args()

USER_OPTION = 47
DETECT_INTERVAL = 5

user_ch = None
start = None

print("PiDown: connecting...")

vehicle = connect(
            args.connect,
            baud=args.baudrate,
            source_system=args.system,
            timeout=args.timeout,
            wait_ready=["parameters"])

print("PiDown: connected")

def msg(txt):
    global vehicle
    vehicle.message_factory.statustext_send(0, txt.encode())

msg("PiDown: started")

@vehicle.on_message("RC_CHANNELS")
def listener(self, name, message):
    global start, user_ch, vehicle, DETECT_INTERVAL
    if user_ch is None:
        return
    if vehicle.channels[user_ch] >= 1800 and start is None:
        start = time.time()
        msg("RPi will shutdown")
        print("PiDown: shutdown ch high")
    if vehicle.channels[user_ch] < 1800 and start is not None:
        start = None
        msg("RPi shutdown canceled")
        print("PiDown: shutdown ch low")

def findCh():
    global user_ch
    for ch in range(1, 17):
        if vehicle.parameters["RC%d_OPTION" % ch] == USER_OPTION:
            user_ch = ch
            break
    return user_ch

while findCh() is None:
    time.sleep(5)

msg("PiDown: shutdown ch %d" % user_ch)

while True:
    if start is not None and time.time() - start >= DETECT_INTERVAL:
        # Shutdown call
        print("PiDown: shutdown detected!")
        call(["shutdown", "-h", "now"], shell=False)
    else:
        time.sleep(0.1)
