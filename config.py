import configparser
import os

config = configparser.ConfigParser()
config.read(os.getcwd() + "/config.ini")