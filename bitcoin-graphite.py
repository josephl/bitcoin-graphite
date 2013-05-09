#!/usr/bin/python

import sys
import time
import requests
import json
from socket import socket


CARBON_SERVER = '127.0.0.1'
CARBON_PORT = 2003
TICKER = 'https://data.mtgox.com/api/1/BTCUSD/ticker'
DELAY = 30 

def requestBitcoin():
    reqData = requests.get(TICKER)
    bitcoinData = json.loads(reqData.content)
    values = bitcoinValues(bitcoinData['return'])
    return values

def bitcoinValues(requestData):
    values = {}
    now = int(requestData.pop('now')) / 1000000
    for key in requestData.keys():
        if (type(requestData[key]) == dict and
                requestData[key].has_key('value')):
            values.update({ key: float(requestData[key]['value']) })
    return metricOutput(values, now)

def metricOutput(values, timestamp):
    lines = []
    for key in values.keys():
        lines.append('bitcoin.%s %f %d' % (key, values[key], timestamp))
    return '\n'.join(lines) + '\n'

def main():
    global DELAY
    if len(sys.argv) > 1:
        DELAY = int(sys.argv[1])

    sock = socket()
    try:
        sock.connect((CARBON_SERVER,CARBON_PORT))
    except:
        print "Couldn't connect to  %(server)s on port %(port)d, " \
            "is carbon-agent.py running?" % {
            'server':CARBON_SERVER, 'port':CARBON_PORT }
        sys.exit(1)

    while True:
        sock.sendall(requestBitcoin())
        time.sleep(DELAY)

if __name__ == '__main__':
    main()
