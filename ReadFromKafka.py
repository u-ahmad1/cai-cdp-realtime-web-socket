import json
import logging
import socket
from json import JSONDecodeError

import tornado
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.websocket import WebSocketHandler

from ReadConfiguration import get_value_from_configuration

consumer = None


def read_data_from_kafka():
    kafka_topic = get_value_from_configuration('kafka.topic')
    kafka_server = get_value_from_configuration('kafka.bootstrap_server')
    offset = get_value_from_configuration('kafka.offset')
    logging.info('Reading data from the kafka with the offset [%s]', offset)

    try:
        global consumer
        consumer = KafkaConsumer(
            kafka_topic,
            bootstrap_servers=[kafka_server],
            auto_offset_reset=offset,
            value_deserializer=lambda m: json.loads(m.decode('ascii')))
    except NoBrokersAvailable:
        logging.error('None of the specified broker is available! please check the bootstrap server in config.')
    except JSONDecodeError:
        logging.error('Current object is not a json object.')
    except Exception as e:
        logging.error(e)


class WSHandler(WebSocketHandler):
    def open(self):
        print('new connection')
        if consumer is not None:
            for msg in consumer:
                print(msg.value)
                self.write_message(msg.value)

    def on_message(self, message):
        print('message received:  %s' % message)
        # Reverse Message and send it back

    def on_close(self):
        print('connection closed')

    def check_origin(self, origin):
        return True


application = Application([
    (r'/ws', WSHandler),
])

if __name__ == "__main__":
    version = '{version 0.1.0}'
    module = '{Kafka Socket:}'
    import os

    if not os.path.exists('logs'):
        os.makedirs('logs')
    logging.basicConfig(filename='logs/suricata.log', level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s:%(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')

    read_data_from_kafka()
    http_server = HTTPServer(application)
    http_server.listen(8888)
    myIP = socket.gethostbyname(socket.gethostname())
    print('*** Websocket Server Started at %s***' % myIP)
    IOLoop.instance().start()
