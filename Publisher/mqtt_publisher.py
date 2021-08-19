# MQTT Publish Demo

import time
import sys

from mqtt_client import MqttClient
from helpers import split_by_size

import config


def publish(file_path, topic):
    client = MqttClient(config.HOST, config.USER, config.PW)

    start = time.time()
    list_of_payloads = split_by_size(file_path)
    success = client.send_multiple_messages(list_of_payloads, topic)
    end = time.time()

    if success:
        mssg = '\nAll segments sent!'
    else:
        mssg = '\nAn error was found while publishing'
    elapsed = end - start
    print(mssg)
    print('Elapsed time:', elapsed, 'seconds')


if __name__ == "__main__":
    file = "paquete_vacio"
    publish(file, sys.argv[1])
