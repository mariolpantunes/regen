# coding: utf-8


__author__ = "Mário Antunes"
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Mário Antunes"
__email__ = "mariolpantunes@gmail.com"
__status__ = "Development"


import json
import time
import socket
import signal
import logging
import argparse
import datetime
from influxdb import InfluxDBClient
from logging.handlers import RotatingFileHandler


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%m-%d %H:%M:%S')
logger = logging.getLogger('RFComm')
handler = logging.handlers.SysLogHandler(address = '/dev/log')
logger.addHandler(handler)


done = False


def exit_gracefully(signum, frame):
    global done
    done = True
    logger.info('Exit gracefully...')


def main(args):
    signal.signal(signal.SIGINT, exit_gracefully)
    signal.signal(signal.SIGTERM, exit_gracefully)

    global done

    while not done:
        try:
            client = InfluxDBClient('localhost', 8086, '', '', 'regen')
            s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
            s.settimeout(5)
            s.connect((args.addr, 1))

            while not done:
                packet = ''
                while not packet or packet[-1] != '}': 
                    data = s.recv(256)
                    packet += data.decode('utf-8')
                jdata = json.loads(packet)
                logger.debug('JSON %s', jdata)

                current_time = datetime.datetime.utcnow().isoformat()
                json_body = [{'measurement':'voltage',
                    'tags':{'address':args.addr},
                    'time':current_time,
                    'fields':{'value': float(jdata['voltage'])}},
                    {'measurement':'ampere',
                    'tags':{'address':args.addr},
                    'time':current_time,
                    'fields':{'value': float(jdata['ampere'])}},
                    {'measurement':'watt',
                    'tags':{'address':args.addr},
                    'time':current_time,
                    'fields':{'value': float(jdata['watt'])}}]
                logger.debug('JSON BODY %s', json_body)
                client.write_points(json_body, time_precision='ms')
                time.sleep(5)

        except Exception as e:
            logger.error('%s', e)
            time.sleep(10)
                
    s.close()
    client.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='RFComm - Reads data from the bt')
    parser.add_argument('--addr', type=str, help='target address', default='FC:A8:9A:00:52:7E')
    args = parser.parse_args()
    main(args)

