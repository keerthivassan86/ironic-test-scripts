"""
service profile modification 
"""

def sp_template_create(handle, name, type, resolve_remote, descr="",
                       usr_lbl="", src_templ_name="", ext_ip_state="none",
                       ext_ip_pool_name="", ident_pool_name="",
                       agent_policy_name="",
                       bios_profile_name="",
                       boot_policy_name="",
                       dynamic_con_policy_name="",
                       host_fw_policy_name="",
                       kvm_mgmt_policy_name="",
                       lan_conn_policy_name="",
                       local_disk_policy_name="",
                       maint_policy_name="",
                       mgmt_access_policy_name="",
                       mgmt_fw_policy_name="",
                       power_policy_name="",
                       san_conn_policy_name="",
                       scrub_policy_name="",
                       sol_policy_name="",
                       stats_policy_name="",
                       vcon_profile_name="",
                       vmedia_policy_name="",
                       parent_dn="org-root"):

    from ucsmsdk.mometa.ls.LsServer import LsServer
    from ucsmsdk.mometa.vnic.VnicConnDef import VnicConnDef

    obj = handle.query_dn(parent_dn)
    if not obj:
        raise ValueError("org '%s' does not exist." % parent_dn)
    mo = LsServer(parent_mo_or_dn=obj,
                  name=name,
                  type=type,
                  resolve_remote=resolve_remote,
                  descr=descr,
                  usr_lbl=usr_lbl,
                  src_templ_name=src_templ_name,
                  ext_ip_state=ext_ip_state,
                  ext_ip_pool_name=ext_ip_pool_name,
                  ident_pool_name=ident_pool_name,
                  vcon_profile_name=vcon_profile_name,
                  agent_policy_name=agent_policy_name,
                  bios_profile_name=bios_profile_name,
                  boot_policy_name=boot_policy_name,
                  dynamic_con_policy_name=dynamic_con_policy_name,
                  host_fw_policy_name=host_fw_policy_name,
                  kvm_mgmt_policy_name=kvm_mgmt_policy_name,
                  local_disk_policy_name=local_disk_policy_name,
                  maint_policy_name=maint_policy_name,
                  mgmt_access_policy_name=mgmt_access_policy_name,
                  mgmt_fw_policy_name=mgmt_fw_policy_name,
                  power_policy_name=power_policy_name,
                  scrub_policy_name=scrub_policy_name,
                  sol_policy_name=sol_policy_name,
                  stats_policy_name=stats_policy_name,
                  vmedia_policy_name=vmedia_policy_name
                  )
    
    vnicConnDefMo = VnicConnDef(parent_mo_or_dn=mo,
                                lan_conn_policy_name=lan_conn_policy_name,
                                san_conn_policy_name=san_conn_policy_name)

    handle.add_mo(mo, True)
    handle.commit()
    return mo


def sp_template_modify(handle, name, type=None, resolve_remote=None,
                       descr=None, usr_lbl=None, src_templ_name=None,
                       ext_ip_state=None, ext_ip_pool_name=None,
                       ident_pool_name=None, vcon_profile_name=None,
                       agent_policy_name=None, bios_profile_name=None,
                       boot_policy_name=None, dynamic_con_policy_name=None,
                       host_fw_policy_name=None, kvm_mgmt_policy_name=None,
                       local_disk_policy_name=None, maint_policy_name=None,
                       mgmt_access_policy_name=None, mgmt_fw_policy_name=None,
                       power_policy_name=None, scrub_policy_name=None,
                       sol_policy_name=None, stats_policy_name=None,
                       vmedia_policy_name=None,
                       parent_dn="org-root"):

    dn = parent_dn + "/ls-" + name
    mo = handle.query_dn(dn)
    if not mo:
        raise ValueError("SP '%s' does not exist" % dn)

    if type is not None:
        mo.type = type
    if resolve_remote is not None:
        mo.resolve_remote = resolve_remote
    if descr is not None:
        mo.descr = descr
    if usr_lbl is not None:
        mo.usr_lbl = usr_lbl
    if src_templ_name is not None:
        mo.src_templ_name = src_templ_name
    if ext_ip_state is not None:
        mo.ext_ip_state = ext_ip_state
    if ext_ip_pool_name is not None:
        mo.ext_ip_pool_name = ext_ip_pool_name
    if ident_pool_name is not None:
        mo.ident_pool_name = ident_pool_name
    if vcon_profile_name is not None:
        mo.vcon_profile_name = vcon_profile_name
    if agent_policy_name is not None:
        mo.agent_policy_name = agent_policy_name
    if bios_profile_name is not None:
        mo.bios_profile_name = bios_profile_name
    if boot_policy_name is not None:
        mo.boot_policy_name = boot_policy_name
    if dynamic_con_policy_name is not None:
        mo.dynamic_con_policy_name = dynamic_con_policy_name
    if host_fw_policy_name is not None:
        mo.host_fw_policy_name = host_fw_policy_name
    if kvm_mgmt_policy_name is not None:
        mo.kvm_mgmt_policy_name = kvm_mgmt_policy_name
    if local_disk_policy_name is not None:
        mo.local_disk_policy_name = local_disk_policy_name
    if maint_policy_name is not None:
        mo.maint_policy_name = maint_policy_name
    if mgmt_access_policy_name is not None:
        mo.mgmt_access_policy_name = mgmt_access_policy_name
    if mgmt_fw_policy_name is not None:
        mo.mgmt_fw_policy_name = mgmt_fw_policy_name
    if power_policy_name is not None:
        mo.power_policy_name = power_policy_name
    if scrub_policy_name is not None:
        mo.scrub_policy_name = scrub_policy_name
    if sol_policy_name is not None:
        mo.sol_policy_name = sol_policy_name
    if stats_policy_name is not None:
        mo.stats_policy_name = stats_policy_name
    if vmedia_policy_name is not None:
        mo.vmedia_policy_name = vmedia_policy_name

    handle.set_mo(mo)
    handle.commit()
    return mo



