---
---

{{% section %}}

# Do's and Don'ts

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

## Minimize paper trail

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
