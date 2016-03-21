import os
import time
import pdb
from ucsmsdk import *
from ucsmsdk import ucshandle
from config import IP,USERNAME,PASSWORD,DN
import Network as mynet
"""
Identifying Network interface changes inside UCSM
"""

def main():

    handle=ucshandle.UcsHandle(IP,username=USERNAME,password=PASSWORD)
    handle.login()

    network=mynet.Network(DN,handle)
    network.get_vnic_templates()

if __name__ == "__main__":
    main()
