#!/usr/bin/env python

import getpass
from nornir.init_nornir import InitNornir


def print_credentials(task):
    print(f"{task.host.name} - {task.host.username}/{task.host.password}")


nr = InitNornir(
    inventory={
        "plugin": "inv.EncryptedInventory",
        "options": {
            "host_file": "hosts.yaml.gpg",
            "group_file": "groups.yaml.gpg",
            "defaults_file": "defaults.yaml.gpg",
            "passphrase": getpass.getpass('Password:'),
        },
    },
)


nr.run(task=print_credentials)
