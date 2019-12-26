from paho_mqtt_examples.paho_mqtt_client import MQTTClient

client = MQTTClient()

client.connect("mqtt.eclipse.org", 1883, 60)

client.subscribe("paho/test/liliu")

client.loop_forever()
