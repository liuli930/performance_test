import getopt
import logging
import asyncio
import os
import re
import sys

from hbmqtt.client import MQTTClient
from hbmqtt.mqtt.constants import QOS_1


async def connect_publish(client_id, publish_time=5):
    config = {
        'keep_alive': 30,
        'ping_delay': 1,
        'default_qos': 1,
        'default_retain': False,
        'auto_reconnect': True,
        'reconnect_max_interval': 10,
        'reconnect_retries': 2,
    }

    client = MQTTClient(client_id=str(client_id), config=config)

    # connect
    await client.connect('mqtt://mqtt.eclipse.org/')

    # publish
    while True:
        await client.publish(topic="paho/test/liliu", message=bytes(str(client_id), 'utf-8'), qos=QOS_1)

        await asyncio.sleep(publish_time)


def usage():
    print("Usage:%s [-h|-v|-t|-n|-k] [--help|--verbose|--time_interval_publish|--num_clients|--k8s_deploy|--k8s_clients_step] args...." % (sys.argv[0]))


if __name__ == '__main__':
    formatter = "[%(asctime)s] %(name)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=formatter)

    # 增加了可配置的参数
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvt:n:ks:", ["help", "verbose", "time_interval_publish=", "num_clients=", "k8s_deploy", "k8s_clients_step="])

        num_clients = 10
        publish_time = 5
        num_start = 0
        num_end = num_clients - 1
        k8s_deploy = False
        k8s_step = 0

        for o, a in opts:
            if o in ("-v", "--verbose"):
                logging.getLogger().setLevel(logging.DEBUG)
            elif o in ("-h", "--help"):
                usage()
                sys.exit()
            elif o in ("-t", "--time_interval_publish"):
                publish_time = int(a)
            elif o in ("-n", "--num_clients"):
                num_clients = int(a)
            # 增加k8s的配置项
            elif o in ("-k", "--k8s_deploy"):
                k8s_deploy = True
            elif o in ("-s", "--k8s_clients_step"):
                k8s_step = int(a)
            else:
                assert False, "unhandled option"
    except getopt.GetoptError:
        usage()
        sys.exit(1)

    # 如果是部署到k8s机器时，根据机器hostname下标计算每台机器的client_id范围
    if k8s_deploy and k8s_step:
        seq = int(re.search(r'(?<=-)\d+', os.getenv("HOSTNAME", 0)).group())
        num_start = seq * k8s_step
        num_end = (seq + 1) * k8s_step

    tasks = []
    for client_id in range(num_clients)[num_start:num_end]:
        tasks.append(asyncio.ensure_future(connect_publish(client_id, publish_time)))

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
