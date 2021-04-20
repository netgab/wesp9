#!/usr/bin/env python3
#! -*- coding: utf-8 -*-

"""
ToDo
"""

# Imports
## Standard: Mandatory generic modules 
import os
import sys
import socket
import logging
from datetime import datetime
import statistics
import json
import time
from pathlib import Path
import getpass

## Custon modules
import wesp9Lib.cliParser as cliParser
import wesp9Lib.connection as connection


# CONSTANTS ###################################################################
# Static
PROGRAM_NAME_SHORT = "Wireless Endpoint Statistics Ping for Catalyst 9800"
PROGRAM_NAME_SHORT = "wesp9"
PROGRAM_VERSION = "0.01.00"

# Dynamic
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
SCRIPT_NAME = os.path.basename(__file__)
HOST_NAME = socket.gethostname()
USER_NAME = getpass.getuser()
###############################################################################

# Logging: Basic configuration ################################################
# Log levels: Requires logging module
LOG_FORMAT_DEFAULT = '%(asctime)s - %(name)s - %(threadName)s - \
  %(levelname)s - %(message)s'
LOG_LEVEL_ERROR = logging.ERROR
LOG_LEVEL_WARN = logging.WARN
LOG_LEVEL_INFO = logging.INFO
LOG_LEVEL_DEBUG = logging.DEBUG
LOG_LEVEL = LOG_LEVEL_WARN

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)

###############################################################################

# Initialize command line parser
wesp9Cli = cliParser.cliArguments()
wesp9Cli.defaultUsername = USER_NAME
if wesp9Cli.version:
  print(f'{PROGRAM_NAME_SHORT} version {PROGRAM_VERSION}')
  sys.exit()

# Logger global configuration #################################################
# Log level
if wesp9Cli.verbose >= 3:
  logLevel = LOG_LEVEL_DEBUG
elif wesp9Cli.verbose == 2:
  logLevel = LOG_LEVEL_INFO
elif wesp9Cli.verbose == 1:
  logLevel = LOG_LEVEL_WARN
else:
  logLevel = LOG_LEVEL_ERROR

# Change log level
logger.setLevel(logLevel)
logging.basicConfig(level=logLevel, format=LOG_FORMAT_DEFAULT)

###############################################################################

def main():
  logger.info(f'SCRIPT_DIR: {SCRIPT_DIR}')
  logger.info(f'SCRIPT_NAME: {SCRIPT_NAME}')
  logger.info(f'HOST_NAME: {HOST_NAME}')

  ## Prompt for password if not passed as command line argument
  if not wesp9Cli.password:
    password = getpass.getpass(f'Password for user {wesp9Cli.username}: ')
  else:
    password = wesp9Cli.password

  # Connect to WLC
  wlcConnection = connection.restconf(
    wlc=wesp9Cli.wlc,
    username=wesp9Cli.username,
    password=password)
  wlcConnection.insecure = wesp9Cli.insecure


  snrList = []
  rssiList = []
  speedList = []
  try:
    while True:
      wlcClientStats = wlcConnection.getClientStats(clientMac=wesp9Cli.client)

      # Add values to list to get min/max/mean values
      snrList.append(wlcClientStats.snr)
      rssiList.append(wlcClientStats.rssi)
      speedList.append(wlcClientStats.speed)
      print(f'{datetime.now()} '\
        f'[{wlcClientStats.clientMac}] AP name={wlcClientStats.apName}  ' \
        f'AP mac={wlcClientStats.apMac}  SSID={wlcClientStats.ssid}  '\
        f'Channel={wlcClientStats.channel}  '\
        f'RSSI={wlcClientStats.rssi} dBm  SNR={wlcClientStats.snr} db  '\
        f'Speed={wlcClientStats.speed} MBit/s  '\
        f'BytesTx/Rx={wlcClientStats.bytesTx}/{wlcClientStats.bytesRx}')

      time.sleep(wesp9Cli.interval)
  except KeyboardInterrupt:
    print('')
    print(f'\nClient statistic for {wlcClientStats.clientMac}')
    print(f'\tRSSI\tmax={max(rssiList)} dBm\t\tmin={min(rssiList)} dBm\t\t'\
       f'average={statistics.mean(rssiList)} dBm')
    print(f'\tSNR\tmax={max(snrList)} dB\t\tmin={min(snrList)} dB\t\t'\
       f'average={statistics.mean(snrList)} dB')
    print(f'\tSpeed\tmax={max(speedList)} MBit/s\t\t'\
       f'min={min(speedList)} MBit/s\t\t'\
       f'average={statistics.mean(speedList)} MBit/s')



if __name__ == "__main__":
    # execute only if run as a script
    main()

    # Change logging for ping output
    logger.info(f'Done')
