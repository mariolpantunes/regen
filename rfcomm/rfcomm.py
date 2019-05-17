# coding: utf-8


__author__ = 'Mário Antunes'
__license__ = 'MIT'
__version__ = '0.1'
__maintainer__ = 'Mário Antunes'
__email__ = 'mariolpantunes@gmail.com'
__status__ = 'Development'


import json
import time
import socket
import signal
import logging
import argparse
import datetime
from logging import handlers
from influxdb import InfluxDBClient


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%m-%d %H:%M:%S')
logger = logging.getLogger('RFComm')
handler = handlers.SysLogHandler(address = '/dev/log')
logger.addHandler(handler)


done = False


def exit_gracefully(signum, frame):
    global done
    if not done:
        done = True
        logger.info('Exit gracefully...')


def main(args):
    signal.signal(signal.SIGINT, exit_gracefully)
    signal.signal(signal.SIGTERM, exit_gracefully)

    global done

    while not done:
        try:
            #client = InfluxDBClient('localhost', 8086, '', '', 'regen')
            s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)  
            s.connect((args.addr, args.port))
            s.settimeout(args.timeout)
            
            while not done:
                packet = ''
                while not packet or packet[-1] != '}': 
                    data = s.recv(128)
                    packet += data.decode('utf-8')
                jdata = json.loads(packet)
                logger.debug('JSON %s', jdata)

                current_time = datetime.datetime.utcnow().isoformat()

                a0 = jdata['a0']
                a1 = jdata['a1']
                a2 = jdata['a2']

                json_body = [{'measurement':'voltage',
                    'tags':{'address':args.addr, 'id':'a0'},
                    'time':current_time,
                    'fields':{'value': float(a0['voltage'])}},
                    {'measurement':'voltage',
                    'tags':{'address':args.addr, 'id':'a1'},
                    'time':current_time,
                    'fields':{'value': float(a1['voltage'])}},
                    {'measurement':'voltage',
                    'tags':{'address':args.addr, 'id':'a2'},
                    'time':current_time,
                    'fields':{'value': float(a2['voltage'])}},

                    {'measurement':'ampere',
                    'tags':{'address':args.addr, 'id':'a0'},
                    'time':current_time,
                    'fields':{'value': float(a0['ampere'])}},
                    {'measurement':'ampere',
                    'tags':{'address':args.addr, 'id':'a1'},
                    'time':current_time,
                    'fields':{'value': float(a1['ampere'])}},
                    {'measurement':'ampere',
                    'tags':{'address':args.addr, 'id':'a2'},
                    'time':current_time,
                    'fields':{'value': float(a2['ampere'])}},

                    {'measurement':'watt',
                    'tags':{'address':args.addr, 'id':'a0'},
                    'time':current_time,
                    'fields':{'value': float(a0['watt'])}},
                    {'measurement':'watt',
                    'tags':{'address':args.addr, 'id':'a1'},
                    'time':current_time,
                    'fields':{'value': float(a1['watt'])}},
                    {'measurement':'watt',
                    'tags':{'address':args.addr, 'id':'a2'},
                    'time':current_time,
                    'fields':{'value': float(a2['watt'])}}]
                logger.debug('JSON BODY %s', json_body)
                #client.write_points(json_body, time_precision='ms')
        except Exception as e:
            logger.error('%s', e)
            if not done:
                time.sleep(args.sleep)
        finally:
            s.close()
            #client.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='RFComm - Reads data from the bt')
    parser.add_argument('--addr', type=str, help='target address', default='FC:A8:9A:00:52:7E')
    parser.add_argument('--port', type=int, help='target port', default=1)
    parser.add_argument('--sleep', type=int, help='sleep when device is not transmitting', default=5)
    parser.add_argument('--timeout', type=int, help='timeout for the BT socket', default=10)
    args = parser.parse_args()
    main(args)

