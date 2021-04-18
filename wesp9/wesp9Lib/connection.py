#!/usr/bin/env python3
#! -*- coding: utf-8 -*-

# Imports
## Standard: Mandatory generic modules 
import sys
import logging
import json
import time

## External
import requests
import urllib3

## Custom
from wesp9.wesp9Lib.statisticModels import wirlessClientStatistics

# Create logger
logger = logging.getLogger(__name__)


class restconf:
  RESTCONF_BASEPATH = "/restconf/data"
  RESTCONF_HTTP_HEADERS = {
      "Accept": "application/yang-data+json",
      "Content-Type" : "application/yang-data+json"
  }

  def __init__(self, wlc: str, username: str, password: str) -> None:
    # CONSTANTS
    RESTCONF_PORT = 443
    self.__wlc = wlc
    self.__port = RESTCONF_PORT
    self.__username = username
    self.__password = password
    self.__insecure = False
    
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    self.__restconfSession = requests.Session()

    self.__clientStats = wirlessClientStatistics()

  # Properties (get/set methods) ############################################  @property
  @property
  def baseUrl(self):
      return f'https://{self.__wlc}:{self.__port}{self.RESTCONF_BASEPATH}'

  @property
  def insecure(self):
      return self.__insecure
  @insecure.setter
  def insecure(self, insecure: bool):
      self.__insecure = insecure
      logger.debug(f'Set HTTPs insecure: {self.__insecure}')

  def __restConfCall(self, url: str):

    logger.debug(f'GET request to: {url}')
    try:
      response = self.__restconfSession.get(url, headers=self.RESTCONF_HTTP_HEADERS, auth=(self.__username, self.__password), verify=self.__insecure)
      logger.debug(f'GET response: Code {response.status_code}')
      #response = requests.get(url, headers=self.RESTCONF_HTTP_HEADERS, auth=(self.__username, self.__password), verify=self.__insecure)
    except requests.exceptions.ConnectionError:
      logger.error(f'Could not connect to URL {url}')
      raise
    except:
      raise

    if response.status_code == 200:
      # Everything is ok - return the data
      return response.json()
    else:
      logger.error(f'Could not access resource {url}')
      sys.exit()

  def getClientStats(self, clientMac: str = None):
    #client-oper-data/dot11-oper-data
    CLIENT_COMMON_OPERDATA_KEY_ROOT = 'Cisco-IOS-XE-wireless-client-oper:common-oper-data'
    clientCommonOperData = self.__restConfCall(f'{self.baseUrl}/Cisco-IOS-XE-wireless-client-oper:client-oper-data/common-oper-data={clientMac}')
    logger.debug(f'Raw data {CLIENT_COMMON_OPERDATA_KEY_ROOT}: {clientCommonOperData}')

    CLIENT_DOT11_OPERDATA_KEY_ROOT = 'Cisco-IOS-XE-wireless-client-oper:dot11-oper-data'
    clientDot11OperData = self.__restConfCall(f'{self.baseUrl}/Cisco-IOS-XE-wireless-client-oper:client-oper-data/dot11-oper-data={clientMac}')
    logger.debug(f'Raw data {CLIENT_DOT11_OPERDATA_KEY_ROOT}: {clientDot11OperData}')

    CLIENT_TRAFFIC_STATS_KEY_ROOT = 'Cisco-IOS-XE-wireless-client-oper:traffic-stats'
    clientTrafficStats = self.__restConfCall(f'{self.baseUrl}/Cisco-IOS-XE-wireless-client-oper:client-oper-data/traffic-stats={clientMac}')
    logger.debug(f'Raw data {CLIENT_TRAFFIC_STATS_KEY_ROOT}: {clientTrafficStats}')

    CLIENT_SIFS_DB_KEY_ROOT = 'Cisco-IOS-XE-wireless-client-oper:sisf-db-mac'
    clientSifsDb = self.__restConfCall(f'{self.baseUrl}/Cisco-IOS-XE-wireless-client-oper:client-oper-data/sisf-db-mac={clientMac}')
    logger.debug(f'Raw data {CLIENT_SIFS_DB_KEY_ROOT}: {clientSifsDb}')


    # Assemble data into result class
    ## common-oper-data
    self.__clientStats.clientMac = clientCommonOperData[CLIENT_COMMON_OPERDATA_KEY_ROOT]['client-mac']
    self.__clientStats.username = clientCommonOperData[CLIENT_COMMON_OPERDATA_KEY_ROOT]['username']
    self.__clientStats.apName = clientCommonOperData[CLIENT_COMMON_OPERDATA_KEY_ROOT]['ap-name']
    self.__clientStats.wlanId = clientCommonOperData[CLIENT_COMMON_OPERDATA_KEY_ROOT]['wlan-id']
    
    ## dot11-oper-data
    self.__clientStats.apMac = clientDot11OperData[CLIENT_DOT11_OPERDATA_KEY_ROOT]['ap-mac-address']
    self.__clientStats.bssid = clientDot11OperData[CLIENT_DOT11_OPERDATA_KEY_ROOT]['ms-bssid']
    self.__clientStats.channel = clientDot11OperData[CLIENT_DOT11_OPERDATA_KEY_ROOT]['current-channel']
    self.__clientStats.ssid = clientDot11OperData[CLIENT_DOT11_OPERDATA_KEY_ROOT]['vap-ssid']

    ## traffic-stats
    self.__clientStats.bytesRx = clientTrafficStats[CLIENT_TRAFFIC_STATS_KEY_ROOT]['bytes-rx']
    self.__clientStats.bytesTx = clientTrafficStats[CLIENT_TRAFFIC_STATS_KEY_ROOT]['bytes-tx']
    self.__clientStats.packetsRx = clientTrafficStats[CLIENT_TRAFFIC_STATS_KEY_ROOT]['pkts-rx']
    self.__clientStats.packetsTx = clientTrafficStats[CLIENT_TRAFFIC_STATS_KEY_ROOT]['pkts-tx']
    self.__clientStats.rssi = clientTrafficStats[CLIENT_TRAFFIC_STATS_KEY_ROOT]['most-recent-rssi']
    self.__clientStats.snr = clientTrafficStats[CLIENT_TRAFFIC_STATS_KEY_ROOT]['most-recent-snr']
    self.__clientStats.speed = clientTrafficStats[CLIENT_TRAFFIC_STATS_KEY_ROOT]['speed']

    ## SIFS DB: IPv4
    try:
      self.__clientStats.ipv4 = clientSifsDb[CLIENT_SIFS_DB_KEY_ROOT]['ipv4-binding']['ip-key']['ip-addr']
    except KeyError:
      logger.debug(f'No IPv4 found for client {clientMac}')

    ## SIFS DB: IPv6
    try:
      ipv6Addresses = clientSifsDb[CLIENT_SIFS_DB_KEY_ROOT]['ipv6-binding']
      for ipv6Address in ipv6Addresses:
        if ipv6Address['ip-key']['zone-id'] == 0:
          self.__clientStats.ipv6 = ipv6Address['ip-key']['ip-addr']
    except KeyError:
      logger.debug(f'No IPv6 found for client {clientMac}')

    return self.__clientStats

  def getApStats(self, apName: str = None):
    #client-oper-data/dot11-oper-data
    #CLIENT_COMMON_OPERDATA_KEY_ROOT = 'Cisco-IOS-XE-wireless-client-oper:common-oper-data'
    #clientCommonOperData = self.__restConfCall(f'{self.baseUrl}/Cisco-IOS-XE-wireless-client-oper:client-oper-data/common-oper-data={clientMac}')
    #logger.debug(f'Raw data {CLIENT_COMMON_OPERDATA_KEY_ROOT}: {clientCommonOperData}')
    pass

  


#class netconf:
# https://www.cisco.com/c/en/us/td/docs/wireless/controller/technotes/8-8/b_c9800_programmability_telemetry_dg.html#id_89637

#class ssh:
