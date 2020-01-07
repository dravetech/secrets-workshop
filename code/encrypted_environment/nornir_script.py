#!/usr/bin/env python

import os

from nornir.init_nornir import InitNornir


def print_credentials(task):
    print(f"{task.host.name} - {task.host.username}/{task.host.password}")


def load_creds_from_env(nr):
    nr.inventory.defaults.password = os.getenv("DEFAULT_PASSWORD")

    for name, group in nr.inventory.groups.items():
        env_name = f"{name.upper()}_PASSWORD"
        group.password = os.getenv(env_name)


nr = InitNornir(
    inventory={
        "options": {
            "host_file": "../nornir/hosts.yaml",
            "group_file": "../nornir/groups.yaml",
            "defaults_file": "../nornir/defaults.yaml",
        },
    },
)

load_creds_from_env(nr)


nr.run(task=print_credentials)
