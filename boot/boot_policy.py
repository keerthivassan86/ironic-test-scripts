import logging
log = logging.getLogger('ucs')


from ucsmsdk.mometa.lsboot.LsbootVirtualMedia import LsbootVirtualMedia
from ucsmsdk.mometa.lsboot.LsbootStorage import LsbootStorage
from ucsmsdk.mometa.lsboot.LsbootLocalStorage import LsbootLocalStorage
from ucsmsdk.mometa.lsboot.LsbootDefaultLocalImage import \
    LsbootDefaultLocalImage
from ucsmsdk.mometa.lsboot.LsbootLocalHddImage import LsbootLocalHddImage
from ucsmsdk.mometa.lsboot.LsbootUsbFlashStorageImage import \
    LsbootUsbFlashStorageImage
from ucsmsdk.mometa.lsboot.LsbootUsbInternalImage import LsbootUsbInternalImage
from ucsmsdk.mometa.lsboot.LsbootUsbExternalImage import LsbootUsbExternalImage
from ucsmsdk.mometa.lsboot.LsbootPolicy import LsbootPolicy


def boot_policy_create(handle, name, descr="",
                       reboot_on_update="yes",
                       enforce_vnic_name="yes",
                       boot_mode="legacy",
                       parent_dn="org-root", boot_device={}):


    mo = handle.query_dn(parent_dn)
    if mo is None:
        raise ValueError("org '%s' does not exist" % parent_dn)

    mo = LsbootPolicy(parent_mo_or_dn=mo,
                      name=name, descr=descr,
                      reboot_on_update=reboot_on_update,
                      enforce_vnic_name=enforce_vnic_name,
                      boot_mode=boot_mode)
    if boot_device is not None:
        _add_device(handle, mo, boot_device)
    handle.add_mo(mo, modify_present=True)
    handle.commit()
    return mo


def boot_policy_modify(handle, name, descr=None,
                       reboot_on_update=None,
                       enforce_vnic_name=None,
                       boot_mode=None,
                       parent_dn="org-root"):


    dn = parent_dn + "/boot-policy-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise ValueError("boot policy '%s' does not exist" % dn)

    if descr is not None:
        mo.descr = descr
    if reboot_on_update is not None:
        mo.reboot_on_update = reboot_on_update
    if enforce_vnic_name is not None:
        mo.enforce_vnic_name = enforce_vnic_name
    if boot_mode is not None:
        mo.boot_mode = boot_mode

    handle.set_mo(mo)
    handle.commit()
    return mo


def boot_policy_remove(handle, name, parent_dn="org-root"):


    dn = parent_dn + "/boot-policy-" + name
    mo = handle.query_dn(dn)
    if mo is None:
        raise ValueError("boot policy '%s' does not exist" % dn)

    handle.remove_mo(mo)
    handle.commit()


def boot_policy_exist(handle, name, reboot_on_update="yes",
                      enforce_vnic_name="yes", boot_mode="legacy", descr="",
                      parent_dn="org-root"):

    dn = parent_dn + "/boot-policy-" + name
    mo = handle.query_dn(dn)
    if mo:
        if ((boot_mode and mo.boot_mode != boot_mode)
            and
            (reboot_on_update and mo.reboot_on_update != reboot_on_update)
            and
            (enforce_vnic_name and mo.enforce_vnic_name != enforce_vnic_name)):
            return False
        return True
    return False


def _add_device(handle, parent_mo, boot_device):
    count = 0
    children = handle.query_children(parent_mo)
    for child in children:
        if hasattr(child, 'order'):
            order = getattr(child, 'order')
            if not order in boot_device:
                log.debug("Deleting boot device from boot policy: %s",
                          child.dn)
                handle.remove_mo(child)
                
    for k in boot_device.keys():
        log.debug("Add boot device: order=%s, %s", k, boot_device[k])
        if boot_device[k] in ["cdrom-local", "cdrom"]:
            _add_cdrom_local(handle, parent_mo, k)
        elif boot_device[k] == "cdrom-cimc":
            _add_cdrom_cimc(handle, parent_mo, k)
        elif boot_device[k] == "cdrom-remote":
            _add_cdrom_remote(handle, parent_mo, k)
        elif boot_device[k] in ["lun", "local-disk", "sd-card", "usb-internal",
                                "usb-external"]:
            if count == 0:
                mo = LsbootStorage(parent_mo_or_dn=parent_mo, order=k)
                mo_1 = LsbootLocalStorage(parent_mo_or_dn=mo)
                count +=1
            if boot_device[k] == "lun":
                _add_local_lun(handle, mo_1, k)
            elif boot_device[k] == "local-disk":
                _add_local_disk(handle, mo_1, k)
            elif boot_device[k] == "sd-card":
                _add_sd_card(handle, mo_1, k)
            elif boot_device[k] == "usb-internal":
                _add_usb_internal(handle, mo_1, k)
            elif boot_device[k] == "usb-external":
                _add_usb_external(handle, mo_1, k)
        elif boot_device[k] in ["floppy", "floppy-local"]:
            _add_floppy_local(handle, parent_mo, k)
        elif boot_device[k] == "floppy-external":
            _add_floppy_remote(handle, parent_mo, k)
        elif boot_device[k] == "virtual-drive":
            _add_virtual_drive(handle, parent_mo, k)
        else:
            log.debug("Option <%s> not recognized." % boot_device[k])


def _add_cdrom_local(handle, parent_mo, order):
    mo = LsbootVirtualMedia(parent_mo_or_dn=parent_mo,
                            access="read-only-local",
                            order=order)


def _add_cdrom_remote(handle, parent_mo ,order):
    mo = LsbootVirtualMedia(parent_mo_or_dn=parent_mo,
                            access="read-only-remote",
                            order=order)

def _add_cdrom_cimc(handle, parent_mo, order):
    mo = LsbootVirtualMedia(parent_mo_or_dn=parent_mo,
                            access="read-only-remote-cimc",
                            order=order)

def _add_floppy_local(handle,parent_mo,order):
    mo = LsbootVirtualMedia(parent_mo_or_dn=parent_mo,
                            access="read-write-local",
                            order=order)


def _add_floppy_remote(handle, parent_mo, order):
    mo = LsbootVirtualMedia(parent_mo_or_dn=parent_mo,
                            access="read-write-remote",
                            order=order)


def _add_virtual_drive(handle, parent_mo, order):
    mo = LsbootVirtualMedia(parent_mo_or_dn=parent_mo,
                            access="read-write-drive",
                            order=order)


def _add_local_disk(handle, parent_mo,order):
    mo_1_1 = LsbootDefaultLocalImage(parent_mo_or_dn=parent_mo, order=order)


def _add_local_lun(handle, parent_mo, order):
    mo_1_1 = LsbootLocalHddImage(parent_mo_or_dn=parent_mo, order=order)


def _add_sd_card(handle, parent_mo, order):
    mo_1_1 = LsbootUsbFlashStorageImage(parent_mo_or_dn=parent_mo, order=order)


def _add_usb_internal(handle, parent_mo,order):
    mo_1_1 = LsbootUsbInternalImage(parent_mo_or_dn=parent_mo, order=order)


def _add_usb_external(handle, parent_mo,order):
    mo_1_1 = LsbootUsbExternalImage(parent_mo_or_dn=parent_mo, order=order)
