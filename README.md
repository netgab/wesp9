# Overview
wesp9 (Wireless Endpoint Statistics Ping) is a simple Python3 program, which
allows to query wireless endpoint statistics from a WLAN controller.

The default "ping-alike" output plots the statistic to the screen in a 
given interval.

**Example**
```
2021-04-19 07:21:39.796661 [00:00:5e:00:53:01] AP name=myAp103  AP mac=a4:b4:39:33:12:22  SSID=mySSID  Channel=132  RSSI=-24 dBm SNR=73 db  Speed=289 MBit/s  BytesTx/Rx=3191/91854
2021-04-19 07:21:42.987372 [00:00:5e:00:53:01] AP name=myAp103  AP mac=a4:b4:39:33:12:22  SSID=mySSID  Channel=132  RSSI=-24 dBm SNR=73 db  Speed=289 MBit/s  BytesTx/Rx=3191/91854
2021-04-19 07:21:46.177063 [00:00:5e:00:53:01] AP name=myAp103  AP mac=a4:b4:39:33:12:22  SSID=mySSID  Channel=132  RSSI=-24 dBm SNR=73 db  Speed=289 MBit/s  BytesTx/Rx=3191/91854
2021-04-19 07:21:49.379410 [00:00:5e:00:53:01] AP name=myAp103  AP mac=a4:b4:39:33:12:22  SSID=mySSID  Channel=132  RSSI=-24 dBm SNR=73 db  Speed=289 MBit/s  BytesTx/Rx=3191/91854
2021-04-19 07:21:52.752491 [00:00:5e:00:53:01] AP name=myAp103  AP mac=a4:b4:39:33:12:22  SSID=mySSID  Channel=132  RSSI=-24 dBm SNR=73 db  Speed=289 MBit/s  BytesTx/Rx=3191/91854
2021-04-19 07:21:55.944053 [00:00:5e:00:53:01] AP name=myAp101  AP mac=88:1d:fc:00:11:22  SSID=mySSID  Channel=100  RSSI=-25 dBm SNR=65 db  Speed=289 MBit/s  BytesTx/Rx=3191/91854
2021-04-19 07:21:59.138387 [00:00:5e:00:53:01] AP name=myAp101  AP mac=88:1d:fc:00:11:22  SSID=mySSID  Channel=100  RSSI=-25 dBm SNR=65 db  Speed=289 MBit/s  BytesTx/Rx=3191/91854
2021-04-19 07:22:02.328027 [00:00:5e:00:53:01] AP name=myAp101  AP mac=88:1d:fc:00:11:22  SSID=mySSID  Channel=100  RSSI=-25 dBm SNR=65 db  Speed=289 MBit/s  BytesTx/Rx=3191/91854
2021-04-19 07:22:05.580912 [00:00:5e:00:53:01] AP name=myAp101  AP mac=88:1d:fc:00:11:22  SSID=mySSID  Channel=100  RSSI=-25 dBm SNR=65 db  Speed=289 MBit/s  BytesTx/Rx=3191/91854
2021-04-19 07:22:08.769321 [00:00:5e:00:53:01] AP name=myAp101  AP mac=88:1d:fc:00:11:22  SSID=mySSID  Channel=100  RSSI=-25 dBm SNR=65 db  Speed=289 MBit/s  BytesTx/Rx=3191/91854
2021-04-19 07:22:11.971076 [00:00:5e:00:53:01] AP name=myAp108  AP mac=a4:b4:39:33:c1:ab  SSID=mySSID  Channel=64  RSSI=-52 dBm SNR=0 db  Speed=289 MBit/s  BytesTx/Rx=3191/91854
2021-04-19 07:22:15.177407 [00:00:5e:00:53:01] AP name=myAp108  AP mac=a4:b4:39:33:c1:ab  SSID=mySSID  Channel=64  RSSI=-52 dBm SNR=0 db  Speed=289 MBit/s  BytesTx/Rx=3191/91854
2021-04-19 07:22:18.424015 [00:00:5e:00:53:01] AP name=myAp108  AP mac=a4:b4:39:33:c1:ab  SSID=mySSID  Channel=64  RSSI=-52 dBm SNR=0 db  Speed=0 MBit/s  BytesTx/Rx=0/0
^C

Client statistic for 00:00:5e:00:53:01
        RSSI    max=-24 dBm             min=-52 dBm             average=-30.846153846153847 dBm
        SNR     max=73 dB               min=0 dB                average=53.07692307692308 dB
        Speed   max=289 MBit/s          min=0 MBit/s            average=266.7692307692308 MBit/s
```



# WLC compatibility
- Catalyst 9800 (tested with version 17.3)

# Protocols
Currently only **RESTCONF** is supported (pull model). `wesp9` communicates 
with the WLC using HTTPS (tcp/443) by default. It is planned to add additional
protocol support like **NETCONF** or streaming telemetry.

# YANG models
For **RESTCONF**, the following YANG models are used to get the statistics:
- Cisco-IOS-XE-wireless-client-oper
  * common-oper-data
    * client MAC address
    * AP name
    * ...
  * dot11-oper-data
    * BSSID
    * channel
    * SSID
    * ...
  * traffic-stats
    * Bytes Tx/Rx
    * SNR
    * RSSI
    * ...
  * sisf-db-mac
    * IPv4 address (collected, but not displayed at the moment)
    * IPv6 address (collected, but not displayed at the moment)

# Usage
**Simple usage**
```bash
python3 wesp9.py -w <C9800-WLC-IPv4> -c <WIRELESS-CLIENT-MAC> -p restconf -k 
```

Example:
```bash
python3 wesp9.py -w myWlc.example.org -c 00:11:22:33:44:55 -p restconf -k 
```

# Dependencies
- Python version: 3.6+
- Python packages
  * requests