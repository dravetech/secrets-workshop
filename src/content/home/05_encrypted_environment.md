---
---

{{% section %}}

1. {{< greyed c="Introduction" >}}
1. {{< greyed c="Do's and Dont's" >}}
1. {{< greyed c="Intro to GnuPG" >}}
1. {{< notgreyed c="Encrypted Environment" >}}
1. {{< greyed c="Encrypted Inventory" >}}
1. {{< greyed c="Hashicorp Vault 101" >}}
1. {{< greyed c="Storing secrets in HCV" >}}
1. {{< greyed c="Building a PKI with HCV" >}}
1. {{< greyed c="Closing thoughts" >}}

---

# Encrypted environment

In this example we are going to use an encrypted file to load environment variables that will only be available to our application.

{{<box class="bs-callout bs-callout-info">}}
Example can be found under <code>./code/encrypted_environment/</code>
{{</box>}}


---

## Environment file

The encrypted file with the secrets can be found in the same folder as `secrets.env.gpg`.

We can verify it's encrypted:

```shell
$ file secrets.env.gpg
secrets.env.gpg: GPG symmetrically encrypted data (AES cipher)
```

---

We can use the `gpg` tool to decrypt the file:

``` shell
$ gpg --decrypt secrets.env.gpg
gpg: AES encrypted data
gpg: encrypted with 1 passphrase
DEFAULT_PASSWORD=this-is-the-default-password
BMA_PASSWORD=this-is=the-password-for-bma
```

{{<box class="bs-callout bs-callout-info">}}
Password for the encrypted file is <code>apassword</code>
{{</box>}}

---

As you probably noticed, we have two environment variables in the file:

* `DEFAULT_PASSWORD` - This is the password we will use unless specified otherwise
* `BMA_PASSWORD` - This is the password we will use for devices in the `bma` group

---

Simple python script to verify we can decrypt and load the environment correctly:

``` python
#!/usr/bin/env python
import os


default = os.getenv("DEFAULT_PASSWORD")
bma = os.getenv("BMA_PASSWORD")

print(f"DEFAULT_PASSWORD = {default}")
print(f"BMA_PASSWORD = {bma}")
```

{{<box class="bs-callout bs-callout-info">}}
Full script can be found in the same folder as <code>script.py</code>
{{</box>}}

---

We can use the `env` command combined with the `gpg` tool to load the environment for our script:

``` shell
$ env $(gpg --decrypt secrets.env.gpg) ./script.py
gpg: AES encrypted data
gpg: encrypted with 1 passphrase
DEFAULT_PASSWORD = this-is-the-default-password
BMA_PASSWORD = this-is=the-password-for-bma
```

---

## Nornir example

As a more elaborate example we are going to see how we can apply what we have seen in this section to a nornir script

---

### Inventory

{{<box class="bs-callout bs-callout-info">}}
Nornir inventory can be found under <code>./code/nornir/</code>
{{</box>}}

---

Hosts:

``` yaml
---
rtr00.bma:
    groups:
        - bma
rtr01.bma:
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
---
bma: {}
cdg: {}
```

Defaults:

``` yaml
---
username: automator
```

---

### Script

1. Create a simple task that will print each device's hostname, username and password
1. Add a short function to load the environment and assign the password to the inventory
1. Run the task over each device

{{<box class="bs-callout bs-callout-info">}}
Full script can be found in the same folder as <code>nornir_script.py</code>
{{</box>}}

---

The task:

``` python
def print_credentials(task):
    print(
        f"{task.host.name} - {task.host.username}/{task.host.password}"
    )
```

---

The function to load the environment:

``` python
def load_creds_from_env(nr):
    nr.inventory.defaults.password = os.getenv("DEFAULT_PASSWORD")

    for name, group in nr.inventory.groups.items():
        env_name = f"{name.upper()}_PASSWORD"
        group.password = os.getenv(env_name)
```

---

Running the task over all the hosts after loading the environment:

``` python
nr = InitNornir(...)

load_creds_from_env(nr)

nr.run(task=print_credentials)
```

---

Running the script:

``` text
$ env $(gpg --decrypt secrets.env.gpg) ./nornir_script.py
gpg: AES encrypted data
gpg: encrypted with 1 passphrase
rtr00.bma - automator/this-is=the-password-for-bma
rtr01.bma - automator/this-is=the-password-for-bma
rtr00.cdg - automator/this-is-the-default-password
rtr01.cdg - automator/this-is-the-default-password

```

---

## Other variants

1. Encrypt/Decrypt using asymmetric encryption
2. Decrypt directly in the python code with [python-gnupg](https://pythonhosted.org/python-gnupg/)
3. Use [pass](https://www.passwordstore.org)


{{% /section %}}
