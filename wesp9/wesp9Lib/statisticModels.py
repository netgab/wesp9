#!/usr/bin/env python3
#! -*- coding: utf-8 -*-

# Imports
## Standard: Mandatory generic modules 
import logging

# Create logger
logger = logging.getLogger(__name__)

class wirlessClientStatistics:
  def __init__(self) -> None:
    self.__clientMac = None
    self.__username = None
    self.__apName = None
    self.__apMac = None
    self.__bssid = None
    self.__ssid = None
    self.__channel = None
    self.__wlanId = None
    self.__bytesTx = None
    self.__bytesRx = None
    self.__packetsTx = None
    self.__packetsRx = None
    self.__rssi = None
    self.__snr = None
    self.__speed = None
    #self.__dataRate = None
    self.__ipv4 = None
    self.__ipv6 = None

  # Properties (get/set methods) ############################################
  @property
  def clientMac(self):
      return self.__clientMac
  @clientMac.setter
  def clientMac(self, macAddress: str):
      self.__clientMac = macAddress
      logger.debug(f'MAC address: {self.__clientMac}')

  @property
  def username(self):
      return self.__username
  @username.setter
  def username(self, macAddress: str):
      self.__username = macAddress
      logger.debug(f'Username: {self.__username}')

  @property
  def apName(self):
      return self.__apName
  @apName.setter
  def apName(self, apName: str):
      self.__apName = apName
      logger.debug(f'AP name: {self.__apName}')

  @property
  def apMac(self):
      return self.__apMac
  @apMac.setter
  def apMac(self, apMac: str):
      self.__apMac = apMac
      logger.debug(f'AP MAC: {self.__apMac}')

  @property
  def bssid(self):
      return self.__bssid
  @bssid.setter
  def bssid(self, bssid: str):
      self.__bssid = bssid
      logger.debug(f'BSSID: {self.__bssid}')

  @property
  def ssid(self):
      return self.__ssid
  @ssid.setter
  def ssid(self, ssid: str):
      self.__ssid = ssid
      logger.debug(f'SSID: {self.__ssid}')

  @property
  def channel(self):
      return self.__channel
  @channel.setter
  def channel(self, channel: str):
      self.__channel = channel
      logger.debug(f'Channel: {self.__channel}')

  @property
  def wlanId(self):
      return self.__wlanId
  @wlanId.setter
  def wlanId(self, wlanId: str):
      self.__wlanId = wlanId
      logger.debug(f'WLAN id: {self.__wlanId}')

  @property
  def bytesTx(self):
      return self.__bytesTx
  @bytesTx.setter
  def bytesTx(self, bytesTx: str):
      self.__bytesTx = bytesTx
      logger.debug(f'Bytes TX: {self.__bytesTx}')

  @property
  def bytesRx(self):
      return self.__bytesRx
  @bytesRx.setter
  def bytesRx(self, bytesRx: str):
      self.__bytesRx = bytesRx
      logger.debug(f'Bytes RX: {self.__bytesRx}')

  @property
  def packetsTx(self):
      return self.__packetsTx
  @packetsTx.setter
  def packetsTx(self, packetsTx: str):
      self.__packetsTx = packetsTx
      logger.debug(f'Packets TX: {self.__packetsTx}')

  @property
  def packetsRx(self):
      return self.__packetsRx
  @packetsRx.setter
  def packetsRx(self, packetsRx: str):
      self.__packetsRx = packetsRx
      logger.debug(f'Packets RX: {self.__packetsRx}')

  @property
  def rssi(self):
      return self.__rssi
  @rssi.setter
  def rssi(self, rssi: str):
      self.__rssi = rssi
      logger.debug(f'RSSI: {self.__rssi}')

  @property
  def snr(self):
      return self.__snr
  @snr.setter
  def snr(self, snr: str):
      self.__snr = snr
      logger.debug(f'SNR: {self.__snr}')

#  @property
#  def dataRate(self):
#      return self.__dataRate
#  @dataRate.setter
#  def dataRate(self, dataRate: str):
#      self.__dataRate = dataRate
#      logger.debug(f'Data rate: {self.__dataRate}')

  @property
  def speed(self):
      return self.__speed
  @speed.setter
  def speed(self, speed: str):
      self.__speed = speed
      logger.debug(f'Speed: {self.__speed}')

  @property
  def ipv4(self):
      return self.__ipv4
  @ipv4.setter
  def ipv4(self, ipv4: str):
      self.__ipv4 = ipv4
      logger.debug(f'IPv4: {self.__ipv4}')

  @property
  def ipv6(self):
      return self.__ipv6
  @ipv6.setter
  def ipv6(self, ipv6: str):
      self.__ipv6 = ipv6
      logger.debug(f'IPv6: {self.__ipv6}')