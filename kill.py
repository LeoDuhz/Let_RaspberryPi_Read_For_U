import os
import configparser

config = configparser.ConfigParser()
config.read('pid.ini')

pid = config.get('pid','pid')
os.system('pkill mplayer')