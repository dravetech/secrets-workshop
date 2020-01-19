---
---

{{% section %}}

1. {{< greyed c="Introduction" >}}
1. {{< greyed c="Do's and Dont's" >}}
1. {{< greyed c="Intro to GnuPG" >}}
1. {{< greyed c="Encrypted Environment" >}}
1. {{< greyed c="Encrypted Inventory" >}}
1. {{< greyed c="Hashicorp Vault 101" >}}
1. {{< notgreyed c="Storing secrets in HCV" >}}
1. {{< greyed c="Building a PKI with HCV" >}}
1. {{< greyed c="Closing thoughts" >}}

---

# HCV: secrets

In this section we are going to:

1. store our passwords in hashicorp's vault
2. store the token to access the vault in an encrypted environment file
3. retrieve the passwords directly in our python code

{{<box class="bs-callout bs-callout-info">}}
Example can be found under <code>./code/hcv_secrets/</code>
{{</box>}}

---

## Starting the dev server

We can start the dev server automatically with `docker-compose up`:

``` txt
$ docker-compose up
Creating network "hcv_secrets_default" with the default driver
Creating hcv_secrets_vault-dev-server_1 ... done
Attaching to hcv_secrets_vault-dev-server_1
vault-dev-server_1  | ==> Vault server configuration:
vault-dev-server_1  |
vault-dev-server_1  |              Api Address: http://0.0.0.0:8200
vault-dev-server_1  |                      Cgo: disabled
vault-dev-server_1  |          Cluster Address: https://0.0.0.0:8201
vault-dev-server_1  |               Listener 1: tcp (addr: "0.0.0.0:8200", cluster addres...
vault-dev-server_1  |                Log Level: info
vault-dev-server_1  |                    Mlock: supported: true, enabled: false
vault-dev-server_1  |            Recovery Mode: false
vault-dev-server_1  |                  Storage: inmem
vault-dev-server_1  |                  Version: Vault v1.3.1
...
```

---

Somewhere in the output you should see the following:

``` txt
The unseal key and root token are displayed below in case you want to
seal/unseal the Vault or re-authenticate.

Unseal Key: WOLKhMovPzj30NsF2ZrAAuVaQ/957lezWWlEOS9/ID4=
Root Token: a-silly-token-for-dev

Development mode should NOT be used in production installations!
```

A reminder this is not suitable for production purposes. It also shows the root token you can use to interact with vault via its API.

---

Now we are going to prepopulate the server with some passwords using the script `init.sh`:

- `defaults` - Our default password if not other password is specified
- `bma` - Our default password for the group `bma`.
- `bma/rtr00` - A specific password for the device `rtr00.bma`

---

``` txt
$ ./init.sh
Token (will be hidden):
Success! You are now authenticated. The token information displayed
below is already stored in the token helper. You do NOT need to run
"vault login" again. Future Vault requests will automatically use this
token.

Key                  Value
---                  -----
token                a-silly-token-for-dev
token_accessor       h4FKkTlzYlQjrJgrvJGwTNRo
token_duration       ∞
token_renewable      false
token_policies       ["root"]
identity_policies    []
policies             ["root"]
...
```

---

## Test script

To demonstrate we can read the passwords from vault we are going to use a test script.

{{<box class="bs-callout bs-callout-info">}}
Full script can be found in the same folder as <code>test_script.py</code>
{{</box>}}

---

Next function will try to find the passwords for a given path or return `None` if none found:

``` python
import hvac

def get_password_from_path(path):
    """
    Return the password if found or None if the path doesn't exist
    """
    client = hvac.Client()
    client.token = os.getenv("HCV_TOKEN")

    try:
        resp = client.secrets.kv.read_secret_version(path=path)
        return resp["data"]["data"].get("password")
    except InvalidPath:
        return None
```

Note that the token for vault is read from the environment. We will pass it via an encrypted file.

---

Now we can use the previous function to retrieve the known paths and print them on the screen:


``` python
print(f"default = {get_password_from_path('defaults')}")
print(f"bma = {get_password_from_path('bma')}")
print(f"bma/rtr00 = {get_password_from_path('bma/rtr00')}")

```

---

As seen previously, we are going to pass the secret via an encrypted environment file by combining the `env` and `gpg` tools :

``` txt
$ gpg --decrypt secrets.env.gpg
gpg: AES encrypted data
gpg: encrypted with 1 passphrase
HCV_TOKEN=a-silly-token-for-dev

$ env $(gpg --decrypt secrets.env.gpg) ./test_script.py
gpg: AES encrypted data
gpg: encrypted with 1 passphrase
default = this-is-the-default-password
bma = this-is-the-password-for-bma
bma/rtr00 = this-is-rtr00-password
```

---

## Nornir script

Now let's combine everything we have seen so far to populate nornir's passwords by reading them from vault.

---

Instead of `load_creds_from_env` we will use a new function that will use the previous function `get_password_from_path` to read the passwords from vault:

``` python
def load_creds_from_hcv(nr):
    nr.inventory.defaults.password = get_password_from_path("defaults")

    for name, group in nr.inventory.groups.items():
        group.password = get_password_from_path(name)
```

---

We need a transform function to populate the passwords for each host:

``` python
def lookup_host_password(host):
    # a hostname can be rtr00.bma so we need to convert it to bma/rtr00
    path = f"{host.name.split('.')[1]}/{host.name.split('.')[0]}"
    host.password = get_password_from_path(path)
```

{{<box class="bs-callout bs-callout-info">}}
A transform function is a function that receives a nornir Host and allows you to manipulate it. Once passed to <code>InitNornir</code>, nornir will make sure it's run on each host.
{{</box>}}

---

``` python
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
```

---

Running the script setting the environment:

``` txt
$ env $(gpg --decrypt secrets.env.gpg) ./nornir_script.py
gpg: AES encrypted data
gpg: encrypted with 1 passphrase
rtr00.bma - automator/this-is-rtr00-password
rtr01.bma - automator/this-is-the-password-for-bma
rtr00.cdg - automator/this-is-the-default-password
rtr01.cdg - automator/this-is-the-default-password
```

{{% /section %}}
