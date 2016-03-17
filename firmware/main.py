import os
import time
from ucsmsdk import *
from ucsmsdk import ucshandle
import Firmware as firm
from config import IP,USERNAME,PASSWORD
def main():
    import pdb
    pdb.set_trace()
    handle=ucshandle.UcsHandle(IP,username=USERNAME,password=PASSWORD)
    handle.login()
    #x = firm.Firmware(handle,dn="org-root/org-Finance")
    #print handle
    #sp=firm.ServiceProfile(handle,"org-root/org-Finance","Welcome-initial") # Template type should be initial not updateable
    #sp.modify_sp()
    #sp.create_fw_policy()
    blade=firm.BladeServer(handle,"org-root/org-Finance",version="2.2(6g)",policy_name="onecloudfirmware")
    #blade.modify_sp()
    blade.discover_blade_server()

if __name__ == "__main__":
    main()
