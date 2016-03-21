import os.path
import sys
import pdb
pdb.set_trace()
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

import time
from ucsmsdk import *
from ucsmsdk import ucshandle
from config import IP,USERNAME,PASSWORD,DN
import Bootpolicy as boot
"""
Identifying Network interface changes inside UCSM
"""

def main():

    handle=ucshandle.UcsHandle(IP,username=USERNAME,password=PASSWORD)
    handle.login()

    myboot=boot.Bootpolicy(DN,handle)
    myboot.policy_create()

if __name__ == "__main__":
    main()
