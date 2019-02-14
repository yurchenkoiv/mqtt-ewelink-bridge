import configparser
import os
import random


def generate_nonce(length):
    return ''.join([str(random.randint(0, 9)) for i in range(length)])


def get_config():
    config = configparser.ConfigParser()
    config.read(os.getcwd() + "/config.ini")
    return config


register_dict = {
    "action": "userOnline",
    "userAgent": "app",
    "version": 6,
    "nonce": generate_nonce(15),
    "apkVersion": "3.2.1",
    "os": get_config().get("phone", "os"),
    "apikey": get_config().get("secrets", "api_key"),
    "ts": "1999999999",
    "model": get_config().get("phone", "model"),
    "romVersion": "6.0.1",
    "sequence": generate_nonce(13)
}

update_dict = {
    "action": "update",
    "userAgent": "app",
    "apikey": get_config().get("secrets", "api_key"),
    "deviceid": None,
    "params": {"switches": [
        # {"outlet": 0,
        #  "switch": None},
        # {"outlet": 1,
        #  "switch": None},
        # {"outlet": 2,
        #  "switch": "on"},
        # {"outlet": 3,
        #  "switch": "on"},
    ]}
}