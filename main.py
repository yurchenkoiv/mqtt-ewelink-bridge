import datetime
import logging

import paho.mqtt.client as mqtt
from config import config
import deviceUtils

MESSAGE_STRING = "{datetime} - message: {message}, topic: {topic}"
devices = []


def on_connect(client, userdata, flags, rc):

    logging.info("() - Connected with result code {}".format(str(datetime.datetime.now()), str(rc)))
    devices_topic = config.items("topics")[0][1]
    for device in devices:
        client.publish(devices_topic, "device name: " + device.device_name + ", switches: " +
                       str([switch for switch in device.device_state.keys()]))

        for switch in device.device_state.keys():
            state_topic = "sonoff/" + device.device_name + "/" + str(switch)
            control_topic = state_topic + "/set"
            client.subscribe(state_topic)
            client.subscribe(control_topic)
            client.publish(state_topic, device.device_state[switch])
            logging.info("{} - Subscribed to: {}".format(str(datetime.datetime.now()), state_topic))


def on_message(client, userdata, message):
    global devices
    if len(message.topic.split("/")) > 2:
        device_name = message.topic.split("/")[1]
        for device in devices:
            if device.device_name == device_name and "set" in message.topic.split("/"):
                new_state = device.change_device_state(str(message.payload.decode("utf-8")),
                                                       int(message.topic.split("/")[-2]))
                client.publish("/".join(message.topic.split("/")[:-1]), new_state)
    logging.info(MESSAGE_STRING.format(datetime=str(datetime.datetime.now()),
                                       message=str(message.payload.decode("utf-8")),
                                       topic=message.topic))


def main():
    client.on_message = on_message
    client.on_connect = on_connect
    client.loop_forever()


if __name__ == "__main__":
    logging.basicConfig(filename="main.log", level=logging.INFO)
    devices = deviceUtils.get_devices()
    client = mqtt.Client()
    client.connect(config.get("mqtt", "ip"), int(config.get("mqtt", "port")))
    main()
