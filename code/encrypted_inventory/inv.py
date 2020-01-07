import os

from nornir.core.deserializer.inventory import Inventory

from gnupg import GPG

import ruamel.yaml


def decrypt_and_load(filename, passphrase):
    # initialize gpg
    gpg = GPG(gnupghome=f"{os.environ['HOME']}/.gnupg")

    # open the encrypted file and decrypt it
    with open(filename, "rb") as f:
        data = gpg.decrypt_file(f, passphrase=passphrase)

    # check for errors
    if not data.ok:
        raise Exception(data.stderr)

    # load the contents as yaml
    yml = ruamel.yaml.YAML(typ="safe")
    return yml.load(data.data)


class EncryptedInventory(Inventory):
    def __init__(self, host_file, group_file, defaults_file, passphrase, *args, **kwargs):
        hosts = decrypt_and_load(host_file, passphrase)
        groups = decrypt_and_load(group_file, passphrase)
        defaults = decrypt_and_load(defaults_file, passphrase)
        super().__init__(hosts=hosts, groups=groups, defaults=defaults, *args, **kwargs)
