#!/usr/bin/env python3

import argparse
import json
import signal
from flask import Flask
import sys
from temper import Temper, USBList

# parsing config
parser = argparse.ArgumentParser()
parser.add_argument("-H", "--host", default="0.0.0.0", help="host to bind to, default: 0.0.0.0")
parser.add_argument("-p", "--port", default=2610, help="port to listen to, default: 2610")
parser.add_argument("-d", "--debug", default=False, help="debug mode, default: False")

args = parser.parse_args()

host = args.host
port = int(args.port)
debug = args.debug

print(f"host = {host}")
print(f"port = {port}")
print(f"debug = {debug}")
print(f"Available endpoints:")
print(f"/list = list available USB devices")
print(f"/metrics = return availale metrics from temper USB devices")

app = Flask("temper")
t = Temper()

@app.route('/list')
def list():
    # re-read USB list in case we have new plugged in device(s)
    usblist = USBList()
    t.usb_devices = usblist.get_usb_devices()

    result = json.dumps(t.usb_devices, indent=2, sort_keys=True)
    return result

@app.route('/metrics')
def metrics():
    # re-read USB list in case we have new plugged in device(s)
    usblist = USBList()
    t.usb_devices = usblist.get_usb_devices()

    result = json.dumps(t.read(), indent=2)
    return result

class GracefulKiller:
  kill_now = False
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)

  def exit_gracefully(self, signum, frame):
    sys.exit(1)

if __name__ == '__main__':
  killer = GracefulKiller()
  while not killer.kill_now:
    app.run(host=host, port=port, debug=debug)
