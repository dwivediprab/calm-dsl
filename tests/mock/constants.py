from calm.dsl.constants import CACHE


class MockConstants:
    MOCK_LOCATION = "tests/mock"
    CACHE_FILE_NAME = "cache_data.json"
    TEST_CONFIG_FILE_NAME = "config_test.json"
    MOCK_JSON_LOCATION = "tests/mock/jsons"
    CACHE_ZIP_FILE_NAME = "cache_data.gz"
    TEST_CONFIG_ZIP_FILE_NAME = "config_test.gz"

    dsl_context = {
        "host": "1.1.1.1",
        "port": "1",
        "username": "usr",
        "password": "pswd",
        "project_name": "default",
        "log_level": "INFO",
        "policy_status": True,
        "approval_policy_status": True,
        "stratos_status": True,
        "retries_enabled": True,
        "connection_timeout": 5,
        "read_timeout": 30,
    }

    linux_cred = {"NAME": "linux_name", "USERNAME": "usr_name", "PASSWORD": "pswd"}

    windows_cred = {"NAME": "windows_name", "USERNAME": "usr_name", "PASSWORD": "pswd"}


    config_json_dummy_data = {
        "AHV": {
            "IMAGES": {
                "DISK": {
                    "CENTOS_HADOOP_MASTER": "Centos7HadoopMaster",
                    "CENTOS_HADOOP_SLAVE": "Centos7HadoopSlave",
                    "CETNOS_BASE": "Centos7-Base",
                    "UBUNTU": "Ubuntu1404",
                    "CENTOS_7_CLOUD_INIT": "CentOS-7-cloudinit",
                    "WINDOWS_SYS_PREP_IMAGE": "Win2k12r2_Sysprep",
                    "WINDOWS_SERVER_2016": "WindowsServer2016",
                    "CENTOS_UEFI_LEGACY_VDISK": "centos74_uefi_legacy_vdisk",
                },
                "CD_ROM": {
                    "SQL_SERVER_2014_x64": "SQLServer2014SP2-FullSlipstream-x64-ENU.iso"
                },
            },
            "NETWORK": {"VLAN1211": "vlan1211", "VLAN800": "vlan.800"},
            "CREDS": {"LINUX": linux_cred, "WINDOWS": windows_cred},
        },
        "EXISTING_MACHINE": {
            "IP_1": "4.4.4.4",
            "IP_2": "5.5.5.5",
            "WIN_IP_ADDR": "6.6.6.6",
            "CREDS": {"LINUX": linux_cred, "WINDOWS": windows_cred},
            "PROTOCOL": "http",
            "PORT": {"SSH": 22, "POWERSHELL": 5985},
            "CONNECTION_TYPE": {"SSH": "SSH", "POWERSHELL": "POWERSHELL"},
            "DUMMY_DATA": {
                "IP_1": "1.1.1.1",
                "CREDS": {
                    "LINUX": {
                        "NAME": "name",
                        "USERNAME": "username",
                        "PASSWORD": "password",
                    },
                    "WINDOWS": {
                        "NAME": "name",
                        "USERNAME": "username",
                        "PASSWORD": "password",
                    },
                },
            },
        },
    }


CONSTANT_ENTITIES = [
    CACHE.ENTITY.USER,
    CACHE.ENTITY.ROLE,
    CACHE.ENTITY.DIRECTORY_SERVICE,
    CACHE.ENTITY.USER_GROUP,
    CACHE.ENTITY.AHV_NETWORK_FUNCTION_CHAIN,
    CACHE.ENTITY.POLICY_EVENT,
    CACHE.ENTITY.POLICY_ACTION_TYPE,
    CACHE.ENTITY.POLICY_ATTRIBUTES,
    CACHE.NDB + CACHE.KEY_SEPARATOR + CACHE.NDB_ENTITY.DATABASE,
    CACHE.NDB + CACHE.KEY_SEPARATOR + CACHE.NDB_ENTITY.PROFILE,
    CACHE.NDB + CACHE.KEY_SEPARATOR + CACHE.NDB_ENTITY.SLA,
    CACHE.NDB + CACHE.KEY_SEPARATOR + CACHE.NDB_ENTITY.CLUSTER,
    CACHE.NDB + CACHE.KEY_SEPARATOR + CACHE.NDB_ENTITY.TIME_MACHINE,
    CACHE.NDB + CACHE.KEY_SEPARATOR + CACHE.NDB_ENTITY.SNAPSHOT,
    CACHE.NDB + CACHE.KEY_SEPARATOR + CACHE.NDB_ENTITY.TAG,
]

PROJECTS = [
    "default",
    "test_snapshot_policy_project",
    "test_vmw_snapshot_policy_project",
    "rbac_bp_test_project",
    "test_approval_policy",
    "test_approval_policy_rbac",
    "test_quota_project",
    "test_dyn_cred_project",
    "test_vpc_project",
]

PROVIDERS = ["AzureVault_Cred_Provider", "HashiCorpVault_Cred_Provider", "NDB"]

SERIALISED_KEYS = [
    "data",
    "auth_schema_list",
    "tags",
    "action_list",
    "accounts_data",
    "whitelisted_subnets",
    "whitelisted_clusters",
    "whitelisted_vpcs",
    "platform_data",
    "slas",
]
