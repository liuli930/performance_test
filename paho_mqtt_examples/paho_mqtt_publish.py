from gevent import monkey

monkey.patch_all()

import gevent

from paho_mqtt_examples.paho_mqtt_client import MQTTClient
import time


def task(pid):
    client = MQTTClient()

    client.connect_async("mqtt.eclipse.org", 1883, 30)

    client.loop_start()
    while True:
        client.publish("paho/test/liliu", payload='payload', qos=1)
        gevent.sleep(20)


threads = []

for i in range(500):
    t = gevent.spawn(task, i)
    time.sleep(0.1)
    threads.append(t)

gevent.joinall(threads)
