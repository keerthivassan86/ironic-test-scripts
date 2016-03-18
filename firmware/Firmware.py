import os
import time
import pdb
from ucsmsdk import *
from ucsmsdk import ucshandle
from ucsmsdk.mometa.firmware.FirmwareComputeHostPack import FirmwareComputeHostPack as firm_pack
from ucsmsdk.mometa.ls.LsServer import LsServer
from ucsmsdk.ucseventhandler import UcsEventHandle
import service_profile as sp
class Firmware(object):
    
    def __init__(self,handle,dn):
        self.handle=handle
        self.dn=dn

    def get_firm_bundle(self,bundle_type=None):     # We are focusing only on blade base bundles
        blade_version=self.version + "B"
        
        if bundle_type is not None:
            filter_str = '(type, %s, type="eq")' % bundle_type
        bundles = self.handle.query_classid(
                class_id="FirmwareDistributable", filter_str=filter_str)
        for bundle in bundles:
            if bundle.version == blade_version:
                return True  
        return False
    
 
        

    def create_fw_policy(self,name):
     	""" 
         Creating firmware policy for the B/C series servers.
        """
        name=None
        print(" ** check for available bundles inside FI")
        
        check_bundle=self.get_firm_bundle(bundle_type="b-series-bundle")
        if check_bundle:
   
            filter_str = '(dn,%s,type="eq")' % self.dn
            dn=self.handle.query_dn(self.dn)
            if dn:
            #check_firmware_exists(self,name)
                mo=firm_pack(parent_mo_or_dn=self.dn,
                                 name=name,
                                 blade_bundle_version="2.2(6g)B",
                                 ignore_comp_check="yes",
                                 update_trigger="immediate")

                self.handle.add_mo(mo,True)
                self.handle.commit()
        return name 
   
    def check_firmware_exists(self,name):
    
        mydn=self.dn + "/fw-host-pack-" + name
        mo = self.handle.query_dn(mydn)
        if mo:
            if ((blade_bundle_version and
                     mo.blade_bundle_version != blade_bundle_version) and (name and mo.name != name)):
                return False
            return True
        return False

    def list_firmware_policy(self):
        firmware_list={} 
        firm_list=self.handle.query_classid("FirmwareComputeHostPack")
        for firm in firm_list:
            if not firm.name in firmware_list:
                firmware_list[firm.name]={'dn':firm.dn,'blade_bundle':firm.blade_bundle_name,'blade_version':firm.blade_bundle_version
                                         }
        return firmware_list   


         
class ServiceProfile(Firmware):
   
    """
       Modify service profile with host firmware policy.
    """
    
    def __init__(self, handle, dn):
        super(ServiceProfile,self).__init__(handle,dn)
          
    
    def modify_sp(self,blade_sp):
        s=self.handle.query_classid("LsServer")
        print("** Querying all service profiles")
        time.sleep(2) 
        xx=[x.__dict__ for x in s if x.assign_state == 'unassigned' and x.assoc_state == 'unassociated' and x.type == 'initial-template']
         
        
        for x in xx:
            print("** Service profile template Name '%s' and type '%s'"%(x['name'],x['type']))
            print("\n")
            print "**Current Service Profile Firmware Policy  '%s'"%(x["oper_host_fw_policy_name"])
            print("\n")
            print("**Check for available firmware policies")
            firmware_list=super(ServiceProfile,self).list_firmware_policy()
            
            if firmware_list.get(self.policy_name):
                print("** Firmware policy <%s> was found "%(self.policy_name)) 
                
                set_flag=False
                user_input=raw_input("** Want to upgrade the firmware version form the current version . Press 'yes' to proceed.")
                if user_input.strip().lower() == "yes":
                    set_flag=True
                    count=0
                    for blade in blade_sp:
                        sp_name=blade['blade']['assigned_to'] 
                        sp_name=sp_name[24:]
                         
                        
                #print("*  %s"%(firmware_list))
                        print("Firmware upgradation is in process for blade<%s>..."%(blade['blade']['blade_dn']))
                        print("Wait for activation")
                        
                        sp.sp_template_modify(self.handle,name=sp_name,usr_lbl=None, src_templ_name=None,ext_ip_state=None,
                                ext_ip_pool_name=x["ext_ip_pool_name"],ident_pool_name=x["ident_pool_name"],vcon_profile_name=None,                                                           agent_policy_name=None,bios_profile_name=None,boot_policy_name="onecloud-uefi",dynamic_con_policy_name=None,                                    host_fw_policy_name=self.policy_name,kvm_mgmt_policy_name=None,local_disk_policy_name=None,
                                maint_policy_name=x["maint_policy_name"],mgmt_access_policy_name=x["mgmt_access_policy_name"],
                                mgmt_fw_policy_name=x["mgmt_fw_policy_name"],power_policy_name=x["power_policy_name"],
                                scrub_policy_name=x["scrub_policy_name"],sol_policy_name=x["sol_policy_name"],
                                stats_policy_name=x["stats_policy_name"],vmedia_policy_name=x["vmedia_policy_name"],parent_dn=self.dn)
                        time.sleep(20)
                 
                else:
                    print("Abort firmware upgradation")
                    break 
            else:
               print("** The firmware policy <%s> was not found in ucsm, try to create a firmware policy"%(self.policy_name))
               if self.check_firmware_exists(self.policy_name):
                   print("** Firmware policy <%s> already exists")
               else:
               
                   self.create_fw_policy(self.policy_name)

class BladeServer(ServiceProfile):

    def __init__(self,handle,dn,version,policy_name):
        super(BladeServer,self).__init__(handle,dn)
        self.handle=handle
        self.dn=dn
        self.version=version
        self.policy_name=policy_name
  
    def discover_blade_server(self):
        b="none"
        blade_sp=[]
        print("Discover blade servers")
        
        filter1='(association,"associated" , type="eq")' 
        filter2='(assigned_to_dn, " ",type="ne")'
        myfilter= filter1 + "and" + filter2 
        list_blades=self.handle.query_classid("ComputeBlade",filter_str=myfilter)  # Fetch the blades , only attached with service profile **
        """
         List only the blades which is associated to Service profile with type Initial
        """
        if list_blades:

            for blade in list_blades:

                myblade={'blade':{'blade_dn':blade.dn,'assigned_to':blade.assigned_to_dn,'association':blade.association}}
                blade_sp.append(myblade)
                mgmt_controllers = self.handle.query_children(in_mo=blade,
                                                 class_id="MgmtController")
                for mo in mgmt_controllers:
                    if mo.subject == "blade":
                        mgmt_controller = mo
                        break

                firmware_running = self.handle.query_children(in_mo=mgmt_controller,    # Check the current firmware version of blades.              
                                                 class_id="FirmwareRunning")               
                for mo in firmware_running:
                    if mo.deployment == "system" or mo.deployment == "boot-loader" and mo.version == self.version:

                        log.debug("Blade <%s> is already at version <%s>" % (blade.dn,
                                                                   mo.version))
                    else:
                        print("current blade <%s> version <%s>"%(blade.dn,mo.version))
                        super(BladeServer,self).modify_sp(blade_sp)                    # Upgrade the firmware version by modifying service Profile.
            
                

                                                                 
        else:
            print("No blade is associated with service profile")
       
