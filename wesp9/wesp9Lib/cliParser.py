#!/usr/bin/env python3
#! -*- coding: utf-8 -*-

# Imports
## Standard: Mandatory generic modules 
import argparse
import logging

# Create logger
logger = logging.getLogger(__name__)


class cliArguments:
    def __init__(self) -> None:
       
        self.__defaultUser = None
        
        # Add command line arguments
        self.addArguments()

        # Print debugging
        self.__debug()
        
    # Properties (get/set methods) ############################################
    @property
    def defaultUsername(self):
        return self.__defaultUser
    @defaultUsername.setter
    def defaultUsername(self, username: str):
        self.__defaultUser = username
        logger.debug(f'Set username to: {self.__defaultUser}')

    @property
    def wlc(self):
        return self.__args.wlc

    @property
    def client(self):
      return self.__args.client

    @property
    def username(self):
      if self.__args.username:
        return self.__args.username
      else:
        return self.__defaultUser

    @property
    def password(self):
      return self.__args.password

    @property
    def interval(self):
        return self.__args.interval

    @property
    def protocol(self):
        return self.__args.protocol 

    @property
    def ap(self):
        return self.__args.ap 

    @property
    def insecure(self):
        return self.__args.insecure 

    @property
    def verbose(self):
        return self.__args.verbose

    @property
    def version(self):
        return self.__args.version

    ###########################################################################
    def addArguments(self):
        cmdArgs = argparse.ArgumentParser()

        # Basis parameters
        cmdArgs.add_argument(
          "-w", "--wlc", required=True, 
          help="Catalyst 9800 WLC IP address or FQDN")

        cmdArgs.add_argument(
          "-c", "--client", required=True, 
          help="Wireless client MAC address (colon syntax)")

        cmdArgs.add_argument(
          "-u", "--username", required=False, default=self.__defaultUser, 
          help="User for WLC RESTCONF authention. If not set, the \
             username of the logged in user is used")

        cmdArgs.add_argument(
          "--password", required=False, 
          help="User password for WLC RESTCONF authention (not recommended). \
            The password is prompted, if not set. Caution: The password will \
              potentially be stored in the shell history.")

        cmdArgs.add_argument(
          "-p", "--protocol", required=False, default="restconf",
          # choices=['restconf', 'netconf', 'ssh'], 
          choices=['restconf'],
          help="Used protocol: (default: restconf)")

        cmdArgs.add_argument(
          "-i", "--interval", required=False, default=3, 
          help="Report interval in seconds (default: 3)")
        
        cmdArgs.add_argument(
          "--ap", required=False, action='store_true',
          help="Report AP statistics")
        
        cmdArgs.add_argument(
          "--version", required=False, action='store_true',
          help="Show wesp9 version" )
        
        cmdArgs.add_argument(
          "-k", "--insecure", required=False, action='store_false',
          help="Allow insecure server connections when using SSL/TLS \
            (RESTCONF)")

        cmdArgs.add_argument(
          "-v", "--verbose", required=False, action="count", default=0,
          help="Verbosity level (-v/-vv/-vvv/-vvv)" )

        self.__args = cmdArgs.parse_args()
    
    def __debug(self):
        logger.debug(f'CLI parameter: wlc -> {self.__args.wlc}')
        logger.debug(f'CLI parameter: client -> {self.__args.client}')
        logger.debug(f'CLI parameter: username -> {self.__args.username}')
        logger.debug(f'CLI parameter: password -> {self.__args.password}')
        logger.debug(f'CLI parameter: protocol -> {self.__args.protocol}')
        logger.debug(f'CLI parameter: interval -> {self.__args.interval}')
        logger.debug(f'CLI parameter: ap -> {self.__args.ap}')
        logger.debug(f'CLI parameter: insecure -> {self.__args.insecure}')
        logger.debug(f'CLI parameter: version -> {self.__args.version}')

###############################################################################
        