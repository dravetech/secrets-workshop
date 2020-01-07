---
---

{{% section %}}

# Introduction

1. Introduction
 1. Disclaimer
 2. What are secrets
1. {{< greyed c="One" >}}
1. {{< greyed c="Two" >}}


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
💡 This applies not only to services but any piece of code that runs without user interaction.
{{</box>}}

{{% /section %}}
