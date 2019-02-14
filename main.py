import os

import paho.mqtt.client as mqtt

import requests
import configparser

from device import Device

devices = []


def on_connect(client, userdata, flags, rc):
    global config

    print("Connected with result code " + str(rc))

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
            print("Subscribed to: " + state_topic)


def on_message(client, userdata, message):
    global devices
    if len(message.topic.split("/")) > 2:
        device_name = message.topic.split("/")[1]
        for device in devices:
            if device.device_name == device_name and "set" in message.topic.split("/"):
                new_state = device.change_device_state(str(message.payload.decode("utf-8")),
                                                       int(message.topic.split("/")[-2]))
                client.publish("/".join(message.topic.split("/")[:-1]), new_state)
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    print("message qos=", message.qos)
    print("message retain flag=", message.retain)


def main():
    global devices, config
    config = configparser.ConfigParser()
    config.read(os.getcwd() + "/config.ini")
    pass
    devices = get_devices()
    client = mqtt.Client()
    client.connect(config.get("mqtt", "ip"), int(config.get("mqtt", "port")))
    client.on_message = on_message
    client.on_connect = on_connect
    client.loop_forever()


def get_devices():
    payload = dict(Authorization='Bearer ' + config.get("secrets", "token"))
    r = requests.get(config.get("urls", "api_url"), headers=payload, verify=False)
    j = r.json()
    devices = []
    for i in range(0, len(j)):
        device_id = j[i]['deviceid']
        device_name = j[i]['name']
        device_state = j[i]['params']['switches']

        devices.append(Device(device_id, device_name, device_state))
    return devices


if __name__ == "__main__":
    main()
