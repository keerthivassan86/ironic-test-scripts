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
Secure boot policy
"""

def main():

    handle=ucshandle.UcsHandle(IP,username=USERNAME,password=PASSWORD)
    handle.login()

    myboot=boot.Bootpolicy(DN,handle)                # Creating boot policy (uefi mode)
    myboot.boot_policy_sp()

if __name__ == "__main__":
    main()
