import os
import time
import pdb
from ucsmsdk import *
from ucsmsdk import ucshandle
from config import IP,USERNAME,PASSWORD
def main():

    handle=ucshandle.UcsHandle(IP,username=USERNAME,password=PASSWORD)
    handle.Login()
    

if __name__ == "__main__":
    main()
