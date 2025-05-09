#!/usr/bin/env python3


import requests
from prometheus_client import start_http_server, Gauge
import time
import signal
import sys

URL = 'http://temper-py:2610/metrics'

def fetch_metrics():
    response = requests.get(URL)
    data = response.json()
    return data

def is_numeric(value):
  try:
    float(value)
    return True
  except:
    return False

gauges = {}
# must be global to ensure we don't create duplicate guage names would result in:
# 'ValueError: Duplicated timeseries in CollectorRegistry'

def process_metrics(data):
  for device in data:
    for key, value in device.items():
      key = key.replace(' ', '_')
      if is_numeric(value) and key not in gauges:
        gauges[key] = Gauge(key, key) #(guage_name, description)
      if is_numeric(value) and key in gauges:
        gauges[key].set(value)


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
    start_http_server(8000)
    while True:
      metrics_data = fetch_metrics()
      process_metrics(metrics_data)
      time.sleep(10)
