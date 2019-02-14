import json
from time import sleep
from websocket import create_connection
from dictionaries import register_dict, update_dict
import logging
from config import config


class States(object):
    ON = "on"
    OFF = "off"


class Device(object):
    def __init__(self, device_id, device_name, device_state):
        logging.basicConfig(filename="device.log", level=logging.INFO)
        self.device_id = int(device_id)
        self.device_name = device_name
        self.device_state = {}
        for device in device_state:
            self.device_state[device["outlet"]] = States.ON if device["switch"] == "on" else States.OFF

    def change_device_state(self, state, outlet):
        if outlet not in [switch for switch in self.device_state.keys()]:
            logging.error("Switch number is out of switches which have current device ({}, "
                          "{}))".format(self.device_id, self.device_name))
        if state not in ["on", "off"]:
            logging.error("Supported states are 'on' and 'off' ({}, "
                          "{}))".format(self.device_id, self.device_name))

        update_dict["deviceid"] = self.device_id
        update_dict["params"]["switches"].append({"outlet": outlet,
                                                  "switch": state})
        websocket = create_connection(config.get("urls", "wss_url"))
        websocket.send(json.dumps(register_dict))
        sleep(.5)
        websocket.send(json.dumps(update_dict))
        websocket.close()
        return state
