---
---

{{% section %}}

1. {{< notgreyed c="Introduction" >}}
1. {{< greyed c="Do's and Dont's" >}}
1. {{< greyed c="Intro to GnuPG" >}}
1. {{< greyed c="Encrypted Environment" >}}
1. {{< greyed c="Encrypted Inventory" >}}
1. {{< greyed c="Hashicorp Vault 101" >}}
1. {{< greyed c="Storing secrets in HCV" >}}
1. {{< greyed c="Building a PKI with HCV" >}}
1. {{< greyed c="Summary" >}}

---

## Disclaimer

This is not a security talk. Even though we will be discussing security topics the aim is on how to consume secrets.

Always be mindful of who you and your company are, the best practices for your industry and always follow the guidelines and instructions from your security team.

---

## What are secrets?

A secret is any piece of information that can be used for authenticating a user or system or to secure information.

Examples of secrets are:

- Passwords
- Tokens
- Private keys
- ~~Usernames~~
- ~~FQDNs~~
- ~~Server ports~~

---

## User secrets

``` shell
localhost $ ssh user@remote.acme.com
user@remote.acme.com's password:
remote #
```

Easy to store and consume, i.e. store in a password manager and enter when requested

---

## Service secrets

``` python
from netmiko import ConnectHandler

params = {
    'device_type': 'cisco_ios',
    'host':   '10.10.10.10',
    'username': 'automator',
    'password': '???',
}
device = ConnectHandler(**params)
...
```
Not so easy to store and consume, needs a store that can be queried and that is secure. This store may require additional authentication.


{{<box class="bs-callout bs-callout-info">}}
This applies not only to services but any piece of code that runs without user interaction.
{{</box>}}

{{% /section %}}
