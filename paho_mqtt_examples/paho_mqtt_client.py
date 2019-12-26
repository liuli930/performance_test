import paho.mqtt.client as mqtt
from utils.logger import logger

class MQTTClient(mqtt.Client):

    def __init__(self, *args,**kwargs):
        super(MQTTClient, self).__init__(*args,**kwargs)
        self.on_connect = self.mqtt_on_connect
        self.on_message = self.mqtt_on_message
        self.on_publish = self.mqtt_on_publish
        self.on_subscribe = self.mqtt_on_subscribe
        self.on_disconnect = self.mqtt_on_disconnect
        # self.on_log=self.mqtt_on_log


    def mqtt_on_connect(self, client, userdata, flags, rc):
        if rc != 0:
            logger.info(f"Mqtt on_connect failed: {mqtt.connack_string(rc)}")
        else:
            logger.info(f"Mqtt on_connect success: {mqtt.connack_string(rc)}")


    def mqtt_on_message(self, client, userdata, message):
        logger.info(f'Mqtt on_message {message.topic} {str(message.qos)} {str(message.payload)}')


    def mqtt_on_publish(self, client, userdata, mid):
        logger.info(f"Mqtt on_publish {mid}")


    def mqtt_on_subscribe(self, client, userdata, mid, granted_qos):
        logger.info(f"Mqtt on_subscribe {str(mid)} {str(granted_qos)}")


    def mqtt_on_disconnect(self, client, userdata, rc):
        if rc != 0:
            logger.info(f"Mqtt on_disconnect failed: {mqtt.error_string(rc)}")
        else:
            logger.info(f"Mqtt on_disconnect success")

    def mqtt_on_log(self, client, userdata, level, buf):
        logger.debug(f"Mqtt on_log {buf}")