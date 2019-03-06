import json
import logging
import socket
import threading
from json import JSONDecodeError

from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application
from tornado.websocket import WebSocketHandler

from ReadConfiguration import get_value_from_configuration

consumer = None
ws_clients = []


class Consumer(threading.Thread):

    def __init__(self):
        super().__init__()
        kafka_topic = get_value_from_configuration('kafka.topic')
        kafka_server = get_value_from_configuration('kafka.bootstrap_server')
        offset = get_value_from_configuration('kafka.offset')
        logging.info('Reading data from the kafka with the offset [%s]', offset)

        try:
            self._consumer = KafkaConsumer(
                kafka_topic,
                bootstrap_servers=[kafka_server],
                auto_offset_reset=offset,
                value_deserializer=lambda m: json.loads(m.decode('ascii')),
                enable_auto_commit=True)
        except NoBrokersAvailable:
            logging.error('None of the specified broker is available! please check the bootstrap server in config.')
        except JSONDecodeError:
            logging.error('Current object is not a json object.')
        except Exception as e:
            logging.error(e)

    def run(self):
        for message in self._consumer:
            WSHandler.write_message_to_clients(message.value)


class WSHandler(WebSocketHandler):

    def open(self):
        print("In open connection")
        if self not in ws_clients:
            ws_clients.append(self)
            print('new connection now have ', len(ws_clients))

    def on_message(self, message):
        print('message received:  %s' % message)
        # Reverse Message and send it back

    def on_close(self):
        print(len(ws_clients))
        if self in ws_clients:
            ws_clients.remove(self)
            print('connection closed')

    def check_origin(self, origin):
        return True

    @classmethod
    def write_message_to_clients(cls, message):
        print("sending message [%s]" % (message,))
        for client in ws_clients:
            client.write_message(message)


application = Application([

    (get_value_from_configuration('socket.name'), WSHandler),
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

    kafka_consumer = Consumer()
    kafka_consumer.start()

    http_server = HTTPServer(application)
    http_server.listen(get_value_from_configuration('socket.port'))
    myIP = socket.gethostbyname(socket.gethostname())
    print('*** Websocket Server Started at %s***' % myIP)
    IOLoop.instance().start()
