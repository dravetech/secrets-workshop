---
---

{{% section %}}

1. {{< greyed c="Introduction" >}}
1. {{< notgreyed c="Do's and Dont's" >}}
1. {{< greyed c="Intro to GnuPG" >}}
1. {{< greyed c="Encrypted Environment" >}}
1. {{< greyed c="Encrypted Inventory" >}}
1. {{< greyed c="Hashicorp Vault 101" >}}
1. {{< greyed c="Storing secrets in HCV" >}}
1. {{< greyed c="Building a PKI with HCV" >}}
1. {{< greyed c="Summary" >}}

---

# Do's and Don'ts

Short tips about things you can do and you should avoid when dealing with secrets.

---

## Use different secrets with tight permissions

- To reduce exposure if a secret is leaked
- To make it easier to rollout new secrets if needed

---

## Minimize paper trail

Your application will always need some secret; certificates, tokens to access external services or even a secret to access your secrets store. Make sure you provide those secrets to your application with little to no paper trail:

``` txt
$ export SOME_SECRET_TOKEN=`cat some_secret_token`
$ ./myapp --some-secret-token $SOME_SECRET_TOKEN
```

Careful with passing secrets in the command line as they will go to the history:

``` txt
$ ./myapp --some-secret-token a-secret-token
history | tail -n 1
2476 ./myapp --some-secret-token a-secret-token
...

```

---

Orchestrators like `kubernetes`, `docker swarm`, etc. have mechanisms to inject secrets into environment variables and files for you, use those capabilities where available!

---

## Do not hardcode secrets

Never hardcode secrets into your application, not even test/dev secrets.

---

![cve-hardcoded-credentials](img/cve.png)

---

## Do not commit secrets to git

If you store the secrets in files, add them to `.gitignore` or, even better, make sure they are outside of a git workspace.

---

![starbucks-leaks-token](img/token_leak.png)

{{% /section %}}
