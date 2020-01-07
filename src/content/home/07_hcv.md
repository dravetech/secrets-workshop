---
---

{{% section %}}

# Hashicorp vault 101

[Hashicorp's vault](https://www.vaultproject.io/), often abbreviated as `hcv`, is a service that allows you to:

{{<box class="bs-callout">}}
secure, store and tightly control access to tokens, passwords, certificates, encryption keys [...] using a UI, CLI, or HTTP API.
{{</box>}}

Service can be interacted with using the CLI, a WEB UI and an API.

---

Storing secrets:


``` txt
$ vault kv put secret/bma/routers/ password=some-secret-password
Key              Value
---              -----
created_time     2020-01-06T17:32:33.690632732Z
deletion_time    n/a
destroyed        false
version          1

$ vault kv put secret/bma/switches password=some-secret-password-b
Key              Value
---              -----
created_time     2020-01-06T17:32:41.891355726Z
deletion_time    n/a
destroyed        false
version          1

$ vault kv put secret/cdg/routers/ password=some-secret-password-c
...
```

---

Listing secrets:

``` txt
$ vault kv list secret
Keys
----
bma/
cdg/

$ vault kv list secret/bma
Keys
----
routers
switches
```

---

Reading secrets:

``` txt
$ vault kv get secret/bma/routers
====== Metadata ======
Key              Value
---              -----
created_time     2020-01-06T17:32:33.690632732Z
deletion_time    n/a
destroyed        false
version          1

====== Data ======
Key         Value
---         -----
password    some-secret-password-a
```

---

Versioning support:

``` txt
$ vault kv put secret/bma/routers password=a-new-password
Key              Value
---              -----
created_time     2020-01-06T17:36:52.977018765Z
deletion_time    n/a
destroyed        false
version          2

$ vault kv get secret/bma/routers
====== Metadata ======
Key              Value
---              -----
created_time     2020-01-06T17:36:52.977018765Z
deletion_time    n/a
destroyed        false
version          2

====== Data ======
Key         Value
---         -----
password    a-new-password
```

---

``` txt

$ vault kv get --version 1 secret/bma/routers
====== Metadata ======
Key              Value
---              -----
created_time     2020-01-06T17:32:33.690632732Z
deletion_time    n/a
destroyed        false
version          1

====== Data ======
Key         Value
---         -----
password    some-secret-password-a

```

---

## Paths

Paths allows you to create hierarchical structures to organize your passwords. For instance:

- `secret/$site` - secrets that apply to devices on a given site
- `secret/$site/$device` - secrets that apply to a given device
- `secret/credentials/$user` - credentials for a given user

Paths support multiple k/v pairs:

``` txt
$ vault kv put secret/dbarroso favorite-color=$COLOR favorite-food=$FOOD
Key              Value
---              -----
created_time     2020-01-06T17:44:20.939288919Z
deletion_time    n/a
destroyed        false
version          1

```

---

## Secrets engines

[Secrets engines](https://www.vaultproject.io/docs/secrets/index.html) are plugins that allow you to generate, store or encrypt data. The default engine allows you to store arbitrary k/v pairs in memory pairs but other secret engines allows you to store them in cloud services, consul, etc., to integrate with Active Directory, Azure, etc., or to generate certificates or ssh keys on demand.

---

## Authentication

Vault support many mechanisms to [authenticate users](https://www.vaultproject.io/docs/auth/index.html); LDAP, radius, JWT, Github, TLS certificates, Tokens, username/passwords...

---

## Policies

[Policies](https://www.vaultproject.io/intro/getting-started/policies.html) allow you to define which actions can be performed on a given path:

``` hcl
# a-sample-policy
path "secret/bma" {
  capabilities = ["create"]
}
path "secret/cdg/routers" {
  capabilities = ["read"]
}
```

Policies can be assigned to users to restrict their access:

``` txt
$ vault write auth/userpass/users/dbarroso policies=admins
```

---

## Seal/Unseal

Vault data is stored encrypted. Unsealing is the act of telling vault how to decrypt the data while sealing is the act of telling vault to forget how to do it. Vault is quite powerful and it allows you to be able to split the keys amongst different users so a single actor can't unseal the service.


---

## Dev server

If you want to play with vault you can:

1. Go to the folder `./code/hcv/` and start a dev server with the command `docker-compose up`
2. On a different shell execute `docker-compose exec vault-dev-server sh`, this should give you access to the docker container running vault
3. In the container execute `vault login` and enter the token `a-silly-token-for-dev`
4. Feel free to try the commands shown in the previous slides
5. Do not forget to stop the environment with `docker-compose down` once you are done.

---

Considerations:

1. The environment provided with this presentation is not ready for production purposes
2. Data is not persisted so stopping the environment will wipe out the secrets
3. There are no users and no policies and the root token is hardcoded


{{% /section %}}
