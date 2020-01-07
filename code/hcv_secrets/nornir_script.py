#!/usr/bin/env python
import os

import hvac
from hvac.exceptions import InvalidPath

from nornir.init_nornir import InitNornir


def print_credentials(task):
    print(f"{task.host.name} - {task.host.username}/{task.host.password}")


def get_password_from_path(path):
    """
    Return the password if found or None if the path doesn't exist
    """
    client = hvac.Client()
    client.token = os.getenv("HCV_TOKEN")

    try:
        resp = client.secrets.kv.read_secret_version(path=path,)
        return resp["data"]["data"].get("password")
    except InvalidPath:
        return None


def load_creds_from_hcv(nr):
    nr.inventory.defaults.password = get_password_from_path("defaults")

    for name, group in nr.inventory.groups.items():
        group.password = get_password_from_path(name)


def lookup_host_password(host):
    # a hostname can be rtr00.bma so we need to convert it to bma/rtr00
    path = f"{host.name.split('.')[1]}/{host.name.split('.')[0]}"
    host.password = get_password_from_path(path)


nr = InitNornir(
    inventory={
        "options": {
            "host_file": "../nornir/hosts.yaml",
            "group_file": "../nornir/groups.yaml",
            "defaults_file": "../nornir/defaults.yaml",
        },
        "transform_function": lookup_host_password,
    },
)

load_creds_from_hcv(nr)


nr.run(task=print_credentials)
