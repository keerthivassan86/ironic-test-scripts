import os
import time
import pdb
from ucsmsdk import *
from ucsmsdk.mometa.fabric.FabricVlan import FabricVlan
from ucsmsdk.mometa.vnic.VnicEtherIf import VnicEtherIf


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

                """
                List the service profile that is only associated with blades.
                """
                blade_sp=self.discover_blade_sp()                 

                for blade in blade_sp:
                    pdb.set_trace()
                    blade_assinment=blade['blade']['assigned_to']
                    print("Vnic Ethernet information")
                    """
                    List all vnics under service profile.
                    """
                    vnic_ether=self.handle.query_children(in_dn=blade_assinment,class_id="VnicEther")
                    for vnic in vnic_ether:
                        vnicc={'dn':vnic.dn,'vnic_name':vnic.name}
                        print "Fetching Vlan information for the VNIC %s"%(blade_assinment+"/ether-"+vnic.name)
                        mydn=blade_assinment + "/ether-" +vnic.name
                        """
                        List all vlans under particular vnic.
                        """
                        vlan_ether=self.handle.query_children(in_dn=mydn,class_id="vnicEtherIf")
                        for vlan in vlan_ether:
                            vlann={'vlan':{'vnic_name':blade_assinment+"/ether-"+vnic.name,'vlan_name':vlan.name,'vlan_net':vlan.vnet,'vnet_dn':vlan.oper_vnet_dn}}
                            print("Available vlans under vnic %s"%(blade_assinment+"/ether-"+vnic.name))
                            print("\n")

                            print("** vlan_name  --- %s vlan_id %s"%(vlan.name,vlan.vnet))

                            if vlan.name == "default":
                                print("Vlan creation is in process")
                                vlan_name="myvlan"
                                """
                                creating new vlan and assign to the vnic.
                                """
                                vlan_creation=vlan_create(self.handle,vlan_name,"4050",parent_dn="fabric/lan")
                                if vlan_creation:
                                    print("vlan %s created sucessfull"%(vlan_name))
                                       
                                    #vlan_delete(self.handle,name="myvlan",parent_dn="fabric/lan") # for deleting the vlan

                                    modify_vlan_if(self.handle,dn=blade_assinment+"/ether-"+vnic.name,child_action=vlan.child_action,config_qualifier=vlan.config_qualifier,default_net="no",flt_aggr=vlan.flt_aggr,name=vlan_name,oper_state=vlan.oper_state,oper_vnet_dn=vlan.oper_vnet_dn,oper_vnet_name=vlan.oper_vnet_name,switch_id=vlan.switch_id,owner=vlan.owner,prop_acl=vlan.prop_acl,
                                           pub_nw_id=vlan.pub_nw_id,rn=vlan.rn,sacl=vlan.sacl,
                                           type=vlan.type,vnet="4050")

                        #vnics.append(vnicc)
        else:
            print("No service profile template found")

        

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

def modify_vlan_if(handle,dn,child_action=None,config_qualifier='',default_net='no',flt_aggr=0,name= None,oper_state=None,oper_vnet_dn=None,
                   oper_vnet_name=None,switch_id=None,owner=None,prop_acl=None,pub_nw_id=None,
                   rn=None,sacl=None,type=None,vnet=None):
    obj=handle.query_dn(dn)
    if obj:
        myvlan= VnicEtherIf(parent_mo_or_dn=obj,default_net=default_net,
                            name=name)
        handle.add_mo(myvlan,modify_present=True)
        handle.commit()
        return myvlan



def vlan_create(handle, name, vlan_id, sharing="none",
                mcast_policy_name="", compression_type="included",
                default_net="no", pub_nw_name="", parent_dn="fabric/lan"):
    obj = handle.query_dn(parent_dn)
    if obj:
        vlan = FabricVlan(parent_mo_or_dn=obj,
                          sharing=sharing,
                          name=name,
                          id=vlan_id,
                          mcast_policy_name=mcast_policy_name,
                          policy_owner="local",
                          default_net=default_net,
                          pub_nw_name=pub_nw_name,
                          compression_type=compression_type)

        handle.add_mo(vlan, modify_present=True)
        handle.commit()
        return vlan

def vlan_delete(handle, name=None,parent_dn="fabric/lan"):
    dn = parent_dn + '/net-' + name
    mo = handle.query_dn(dn)
    if mo:
        handle.remove_mo(mo)
        handle.commit()
    else:
        raise ValueError("VLAN '%s' is not present" % dn)


