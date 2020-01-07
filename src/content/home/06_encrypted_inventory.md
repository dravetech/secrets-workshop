---
---

{{% section %}}

# Encrypted inventory

In this example we are going to encrypt the data we want to consume with ``gpg`` and load it directly from the code.

To demonstrate it we are going to include the secrets in nornir's inventory file, encrypt it and create a custom inventory plugin that will load the encrypted files directly after asking the user for the password.

---

## The inventory

{{<box class="bs-callout bs-callout-info">}}
Password for the encrypted files is <code>apassword</code>
{{</box>}}

---

Hosts:

``` yaml
$ gpg --decrypt hosts.yaml.gpg
gpg: AES encrypted data
gpg: encrypted with 1 passphrase
---
rtr00.bma:
    groups:
        - bma
rtr01,bma:
    groups:
        - bma
rtr00.cdg:
    groups:
        - cdg
rtr01.cdg:
    groups:
        - cdg
```

---

Groups:
``` yaml
$ gpg --decrypt groups.yaml.gpg
gpg: AES encrypted data
gpg: encrypted with 1 passphrase
---
bma:
    password: this-is-the-password-for-bma
cdg: {}
```

Defaults:
``` yaml
$ gpg --decrypt defaults.yaml.gpg
gpg: AES encrypted data
gpg: encrypted with 1 passphrase
---
username: automator
password: this-is-the-default-password
```

---

## The inventory plugin

{{<box class="bs-callout bs-callout-info">}}
Full script can be found in the same folder as <code>inv.py</code>
{{</box>}}

---

``` python
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

```

---

``` python
class EncryptedInventory(Inventory):
    def __init__(
      self, host_file, group_file, defaults_file,
      passphrase, *args, **kwargs,
    ):

        hosts = decrypt_and_load(host_file, passphrase)
        groups = decrypt_and_load(group_file, passphrase)
        defaults = decrypt_and_load(defaults_file, passphrase)

        super().__init__(
          hosts=hosts, groups=groups, defaults=defaults,
          *args, **kwargs
        )
```

---

## The script

``` python
import getpass

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
```

{{<box class="bs-callout bs-callout-info">}}
Full script can be found in the same folder as <code>nornir_script.py</code>
{{</box>}}

---

## Usage

``` shell
$ ./nornir_script.py
Password:
rtr00.bma - automator/this-is-the-password-for-bma
rtr01,bma - automator/this-is-the-password-for-bma
rtr00.cdg - automator/this-is-the-default-password
rtr01.cdg - automator/this-is-the-default-password
```


{{% /section %}}
