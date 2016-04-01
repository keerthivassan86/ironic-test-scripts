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
       #for vnic in list_vnic:
           #print vnic
       #self.get_vlan()
       self.get_sp()

    def get_vlan(self):
        list_vlan=self.handle.query_classid("FabricVlan")
        for vlan in list_vlan:
            print "vlan information is %s"%(vlan)

    def get_sp(self):
        vnics=[]
        sp=self.handle.query_classid("LsServer")
        print("List all service profiles")
        for template in sp:
            print template
        sp_temp=[x.__dict__ for x in sp if x.assign_state == 'unassigned' and x.assoc_state == 'unassociated' and x.type == 'initial-template']
        if sp_temp:
            for s in sp_temp:
                print("service profile template <%s> found"%(s['name']))
                blade_sp=self.discover_blade_sp()

                for blade in blade_sp:
                    pdb.set_trace()
                    blade_assinment=blade['blade']['assigned_to']
                    print("Vnic Ethernet information")
                    vnic_ether=self.handle.query_children(in_dn=blade_assinment,class_id="VnicEther")
                    for vnic in vnic_ether:
                        vnicc={'dn':vnic.dn,'vnic_name':vnic.name}
                        print "Fetching Vlan information for the VNIC %s"%(blade_assinment+"/ether-"+vnic.name)
                        mydn=blade_assinment + "/ether-" +vnic.name
                        vlan_ether=self.handle.query_children(in_dn=mydn,class_id="vnicEtherIf")
                        for vlan in vlan_ether:
                            vlann={'vlan':{'vnic_name':blade_assinment+"/ether-"+vnic.name,'vlan_name':vlan.name,'vlan_net':vlan.vnet,'vnet_dn':vlan.oper_vnet_dn}}
                            print vlann
                        #vnics.append(vnicc)


        else:
            print("No service profile template found")

        print vnics

    def discover_blade_sp(self):
        blade_sp=[]
        print("Discover blade servers associated with sp")
        filter1='(association,"associated" , type="eq")'
        filter2='(assigned_to_dn, " ",type="ne")'
        myfilter= filter1 + "and" + filter2
        list_blades=self.handle.query_classid("ComputeBlade",filter_str=myfilter)
        if list_blades:
            for blade in list_blades:
                myblade={'blade':{'blade_dn':blade.dn,'assigned_to':blade.assigned_to_dn,'association':blade.association}}
                blade_sp.append(myblade)
        else:
            print "No blades associated with sp"
        return blade_sp
