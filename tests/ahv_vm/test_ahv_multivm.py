import json
import pytest

from calm.dsl.builtins import AhvVmDisk, AhvVmNic, AhvVmGC
from calm.dsl.builtins import ref, basic_cred, AhvVmResources, AhvVm
from calm.dsl.builtins import vm_disk_package, read_local_file

from calm.dsl.builtins import Service, Package, Substrate
from calm.dsl.builtins import Deployment, Profile, Blueprint
from calm.dsl.builtins import CalmVariable, CalmTask, action
from calm.dsl.builtins import Metadata, Ref
from calm.dsl.builtins.models.metadata_payload import (
    get_metadata_payload,
    reset_metadata_obj,
)
from calm.dsl.config import get_context


DSL_CONFIG = json.loads(read_local_file(".tests/config.json"))
CENTOS_HM = DSL_CONFIG["AHV"]["IMAGES"]["DISK"]["CENTOS_HADOOP_MASTER"]
CENTOS_CI = DSL_CONFIG["AHV"]["IMAGES"]["DISK"]["CENTOS_7_CLOUD_INIT"]
SQL_SERVER_IMAGE = DSL_CONFIG["AHV"]["IMAGES"]["CD_ROM"]["SQL_SERVER_2014_x64"]
NETWORK1 = DSL_CONFIG["AHV"]["NETWORK"]["VLAN1211"]  # TODO change network constants

# projects
PROJECT_NAME = list(DSL_CONFIG["METADATA"]["PROJECT"].keys())[0]

CENTOS_KEY = read_local_file(".tests/keys/centos")
CENTOS_PUBLIC_KEY = read_local_file(".tests/keys/centos_pub")
DefaultCred = basic_cred("centos", CENTOS_KEY, name="Centos", type="KEY", default=True)

Era_Disk = vm_disk_package(
    name="era_disk",
    config={
        # By default image type is set to DISK_IMAGE
        "image": {
            "source": "http://download.nutanix.com/era/1.1.1/ERA-Server-build-1.1.1-340d9db1118eac81219bec98507d4982045d8799.qcow2"
        }
    },
)
Virtio_CdRom = vm_disk_package(
    name="virtio_cdrom",
    config={
        "image": {
            "type": "ISO_IMAGE",
            "source": "http://10.40.64.33/GoldImages/NuCalm/ISO/Nutanix-VirtIO-1.1.4.iso",
        }
    },
)


class AhvVmService(Service):
    """Sample mysql service"""

    ENV = CalmVariable.Simple("DEV")


class AhvVmPackage(Package):
    """Example package with variables, install tasks and link to service"""

    foo = CalmVariable.Simple("bar")
    services = [ref(AhvVmService)]

    @action
    def __install__():
        CalmTask.Exec.ssh(name="Task1", script="echo @@{foo}@@")


class AhvVmPackage2(AhvVmPackage):
    pass


class MyAhvVmResources(AhvVmResources):

    memory = 4
    vCPUs = 2
    cores_per_vCPU = 1
    disks = [
        AhvVmDisk(CENTOS_HM),
        AhvVmDisk.CdRom(SQL_SERVER_IMAGE),
        AhvVmDisk.CdRom.Sata(SQL_SERVER_IMAGE),
        AhvVmDisk.CdRom.Ide(SQL_SERVER_IMAGE),
        AhvVmDisk.Disk.Scsi.cloneFromImageService(CENTOS_CI),
        AhvVmDisk.Disk.Pci.allocateOnStorageContainer(12),
        AhvVmDisk.CdRom.Sata.emptyCdRom(),
        AhvVmDisk.CdRom.Ide.emptyCdRom(),
        AhvVmDisk.Disk.Scsi.cloneFromVMDiskPackage(Era_Disk, bootable=True),
        AhvVmDisk.CdRom.Sata.cloneFromVMDiskPackage(Virtio_CdRom),
    ]
    nics = [AhvVmNic(NETWORK1), AhvVmNic.DirectNic.egress(NETWORK1)]

    guest_customization = AhvVmGC.CloudInit(
        config={
            "users": [
                {
                    "name": "centos",
                    "ssh-authorized-keys": [CENTOS_PUBLIC_KEY],
                    "sudo": ["ALL=(ALL) NOPASSWD:ALL"],
                }
            ]
        }
    )

    serial_ports = {0: False, 1: False, 2: True, 3: True}


class MyAhvVm(AhvVm):

    resources = MyAhvVmResources
    categories = {"AppFamily": "Backup", "AppType": "Default"}


class AhvVmSubstrate(Substrate):
    """AHV VM config given by reading a spec file"""

    provider_spec = MyAhvVm


class MyAhvVmResources2(AhvVmResources):

    memory = 4
    vCPUs = 2
    cores_per_vCPU = 1
    disks = [
        AhvVmDisk(CENTOS_HM),
        AhvVmDisk.Disk.Pci.cloneFromImageService(CENTOS_CI, bootable=True),
        AhvVmDisk.CdRom.Ide.emptyCdRom(),
    ]
    nics = [AhvVmNic(NETWORK1), AhvVmNic.DirectNic.egress(NETWORK1)]

    guest_customization = AhvVmGC.CloudInit(
        config={
            "users": [
                {
                    "name": "centos",
                    "ssh-authorized-keys": [CENTOS_PUBLIC_KEY],
                    "sudo": ["ALL=(ALL) NOPASSWD:ALL"],
                }
            ]
        }
    )

    serial_ports = {0: False, 1: False, 2: True, 3: True}


class MyAhvVm2(AhvVm):

    resources = MyAhvVmResources2


class AhvVmSubstrate2(Substrate):
    """AHV VM config given by reading a spec file"""

    provider_spec = MyAhvVm2


class AhvVmDeployment(Deployment):
    """Sample deployment pulling in service and substrate references"""

    packages = [ref(AhvVmPackage)]
    substrate = ref(AhvVmSubstrate)


class AhvVmDeployment2(Deployment):
    """Sample deployment pulling in service and substrate references"""

    packages = [ref(AhvVmPackage2)]
    substrate = ref(AhvVmSubstrate2)


class AhvVmProfile(Profile):
    """Sample application profile with variables"""

    nameserver = CalmVariable.Simple("10.40.64.15", label="Local DNS resolver")
    foo1 = CalmVariable.Simple("bar1", runtime=True)
    foo2 = CalmVariable.Simple("bar2", runtime=True)

    deployments = [AhvVmDeployment]

    @action
    def test_profile_action():
        """Sample description for a profile action"""
        CalmTask.Exec.ssh(name="Task5", script='echo "Hello"', target=ref(AhvVmService))


class AhvVmProfile2(Profile):
    """Sample application profile with variables"""

    nameserver = CalmVariable.Simple("10.40.64.15", label="Local DNS resolver")
    foo1 = CalmVariable.Simple("bar1", runtime=True)
    foo2 = CalmVariable.Simple("bar2", runtime=True)

    deployments = [AhvVmDeployment2]

    @action
    def test_profile_action():
        """Sample description for a profile action"""
        CalmTask.Exec.ssh(name="Task5", script='echo "Hello"', target=ref(AhvVmService))


class AhvBlueprint(Blueprint):
    """Sample Bp that used ahv_vm_helpers"""

    credentials = [DefaultCred]
    services = [AhvVmService]
    packages = [AhvVmPackage, AhvVmPackage2, Era_Disk, Virtio_CdRom]
    substrates = [AhvVmSubstrate, AhvVmSubstrate2]
    profiles = [AhvVmProfile, AhvVmProfile2]


class BpMetadata(Metadata):

    project = Ref.Project(PROJECT_NAME)


@pytest.mark.pre_commit
def test_multivm_with_diff_bootconfig():
    """
    Tests in case of multi-vm blueprint, correct disk is set to bootable
    """

    # Ahv Helpers uses Metadata Context, It should the context(if any) defined in this file only
    get_metadata_payload(__file__)
    ContextObj = get_context()
    ContextObj.reset_configuration()

    spec = AhvBlueprint.get_dict()
    substrate_list = spec["substrate_definition_list"]

    # From AhvBlueprint class
    # substrate_list[0] = AhvVmSubstrate and substrate_list[1] = AhvVmSubstrate2

    # In AhvVmSubstrate -> MyAhvVm (vm_cls)
    # Check SCSI disk with device_index = 2 is bootable
    ahv_vm_substrate_spec = substrate_list[0]
    assert ahv_vm_substrate_spec["create_spec"]["resources"]["boot_config"] == {
        "boot_device": {"disk_address": {"device_index": 2, "adapter_type": "SCSI"}}
    }

    # In AhvVmSubstrate2 -> MyAhvVm2 (vm_cls)
    # Check PCI disk with device_index = 0 is bootable
    ahv_vm_substrate2_spec = substrate_list[1]
    assert ahv_vm_substrate2_spec["create_spec"]["resources"]["boot_config"] == {
        "boot_device": {"disk_address": {"device_index": 0, "adapter_type": "PCI"}}
    }

    # reset metadata obj
    reset_metadata_obj()
