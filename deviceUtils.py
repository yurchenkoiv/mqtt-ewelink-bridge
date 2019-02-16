import logging

import requests
from config import config
from device import Device


def get_devices():
    payload = dict(Authorization='Bearer ' + config.get("secrets", "token"))
    r = requests.get(config.get("urls", "api_url"), headers=payload, verify=False)
    j = r.json()
    devices = []
    for i in range(0, len(j)):
        device_id = j[i]['deviceid']
        device_name = j[i]['name']
        if "switches" in j[i]['params']:
            device_state = j[i]['params']['switches']
        else:
            device_state = j[i]['params']['switch']
        devices.append(Device(device_id, device_name, device_state))
    return devices