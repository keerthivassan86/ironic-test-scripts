import os
import time
import pdb
from ucsmsdk import *


class Network(object):

    def __init__(self,dn,handle):
        self.dn=dn
        self.handle=handle

    def get_vnic_templates(self):

       list_vnic=self.handle.query_classid("vnicLanConnTempl")
       for vnic in list_vnic:
           print vnic
       self.get_vlan()

    def get_vlan(self):
        list_vlan=self.handle.query_classid("FabricVlan")
        for vlan in list_vlan:
            print "vlan information is %s"%(vlan)
