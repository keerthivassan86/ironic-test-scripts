import pdb
import time
import os
import sys

from boot_policy import boot_policy_create,boot_policy_exist,boot_policy_modify
from config import BOOT_MODE,BOOT_DEVICE,BOOT_POLICY_NAME
from firmware import service_profile


class Bootpolicy(object):

    def __init__(self,dn,handle):
        self.dn=dn
        self.handle=handle

    def policy_create(self):
        policy_name=None
        print("** initiating boot policy %s creation..."%(BOOT_POLICY_NAME))
        print("\n")
        print("** Checking existing boot policy ")
        policy_exits=boot_policy_exist(self.handle,BOOT_POLICY_NAME,reboot_on_update="yes",boot_mode=BOOT_MODE,parent_dn=self.dn)
        if not policy_exits:
            print("** creating boot policy %s"%(BOOT_POLICY_NAME))
            time.sleep(5)

            # creating boot policy
            policy=boot_policy_create(self.handle,BOOT_POLICY_NAME,reboot_on_update="yes",boot_mode=BOOT_MODE,parent_dn=self.dn,boot_device=BOOT_DEVICE)
            policy_name=BOOT_POLICY_NAME
        else:
            print("** Boot policy <%s> already exists"%(BOOT_POLICY_NAME))
            policy_name=BOOT_POLICY_NAME
        return policy_name

        # Below lines for modifying boot policy "

        #print("Modifying boot policy")
        #policy_modify=boot_policy_modify(self.handle,BOOT_POLICY_NAME,reboot_on_update="yes",boot_mode="uefi",parent_dn=self.dn)

    def boot_policy_sp(self):

        filter1='(association,"associated" , type="eq")'
        filter2='(assigned_to_dn, " ",type="ne")'
        myfilter= filter1 + "and" + filter2
        policy_name=self.policy_create()
        list_blades=self.handle.query_classid("ComputeBlade",filter_str=myfilter)
        if list_blades:
            for blade in list_blades:
                sp_name=blade.assigned_to_dn
                sp_name=sp_name[24:]
                mydn=self.dn + "/ls-" + sp_name
                query=self.handle.query_dn(mydn)
                query_dict=query.__dict__
                print("**  Attaching boot policy <%s> to the service profile"%(policy_name))
                time.sleep(3)
                # Modify the blade service profile
                sp_modify=service_profile.sp_template_modify(self.handle,name=query_dict['name'],usr_lbl=None, src_templ_name=None,ext_ip_state=None,
                                ext_ip_pool_name=query_dict["ext_ip_pool_name"],ident_pool_name=query_dict["ident_pool_name"],vcon_profile_name=None,agent_policy_name=None,bios_profile_name=None,boot_policy_name=policy_name,dynamic_con_policy_name=None,host_fw_policy_name=None,kvm_mgmt_policy_name=None,local_disk_policy_name=None,
                                maint_policy_name=query_dict["maint_policy_name"],mgmt_access_policy_name=query_dict["mgmt_access_policy_name"],
                                mgmt_fw_policy_name=query_dict["mgmt_fw_policy_name"],power_policy_name=query_dict["power_policy_name"],
                                scrub_policy_name=query_dict["scrub_policy_name"],sol_policy_name=query_dict["sol_policy_name"],
                                stats_policy_name=query_dict["stats_policy_name"],vmedia_policy_name=query_dict["vmedia_policy_name"],parent_dn=self.dn)
                if sp_modify:
                    print("** Boot policy <%s> assigned sucessfully to <%s> "%(policy_name,mydn))
                else:
                    print("** Problem in assigning boot policy")

        else:
            print("** No blade associated with service profile")





