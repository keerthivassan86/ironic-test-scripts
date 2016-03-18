

def hfp_create(handle, name, blade_bundle_version,
                         rack_bundle_version,  mode="staged", descr="",
                         parent_dn="org-root"):

    from ucsmsdk.mometa.firmware.FirmwareComputeHostPack import\
        FirmwareComputeHostPack

    org = handle.query_dn(parent_dn)
    if not org:
        raise ValueError("org '%s' does not exist" % parent_dn)

    mo = FirmwareComputeHostPack(parent_mo_or_dn=org.dn,
                                 name=name,
                                 blade_bundle_version=blade_bundle_version,
                                 rack_bundle_version=rack_bundle_version,
                                 mode=mode,
                                 descr=descr
                                 )
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def hfp_modify(handle, name, blade_bundle_version=None,
               rack_bundle_version=None, mode=None, descr=None,
               parent_dn="org-root"):

    dn = parent_dn + "/fw-host-pack-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise ValueError("hfp does not exist.")

    if blade_bundle_version is not None:
        mo.blade_bundle_version = blade_bundle_version
    if rack_bundle_version is not None:
        mo.rack_bundle_version = rack_bundle_version
    if mode is not None:
        mo.mode = mode
    if descr is not None:
        mo.descr = descr

    handle.set_mo(mo)
    handle.commit()
    return mo


def hfp_remove(handle, name, parent_dn="org-root"):


    dn = parent_dn + "/fw-host-pack-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise ValueError("hfp does not exist.")

    handle.remove_mo(mo)
    handle.commit()


def hfp_exists(handle, name, blade_bundle_version, rack_bundle_version,
               mode="staged", descr="", parent_dn="org-root"):

    dn = parent_dn + "/fw-host-pack-" + name
    mo = handle.query_dn(dn)
    if mo:
        if ((blade_bundle_version and
                     mo.blade_bundle_version != blade_bundle_version) and
            (rack_bundle_version and
                     mo.rack_bundle_version != rack_bundle_version) and
            (mode and mo.mode != mode) and
            (descr and mo.descr != descr)):
            return False
        return True
    return False
