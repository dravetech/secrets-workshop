---
---

{{% section %}}

1. {{< greyed c="Introduction" >}}
1. {{< greyed c="Do's and Dont's" >}}
1. {{< greyed c="Intro to GnuPG" >}}
1. {{< greyed c="Encrypted Environment" >}}
1. {{< greyed c="Encrypted Inventory" >}}
1. {{< greyed c="Hashicorp Vault 101" >}}
1. {{< greyed c="Storing secrets in HCV" >}}
1. {{< notgreyed c="Building a PKI with HCV" >}}
1. {{< greyed c="Summary" >}}

---

# PKI

In this section we are going to:

1. Enable a PKI in hashicorp's vault
2. Import a CA certificate
3. Use ``vault``'s cli to interact with the PKI
4. Use a simple python script to generate certificates on-demand


{{<box class="bs-callout bs-callout-info">}}
Example can be found under <code>./code/hcv_pki/</code>
{{</box>}}

---

## Starting vault

Like in previous examples, you can start vault with `docker-compose up`

``` txt
$ docker-compose up
Starting hcv_pki_vault-dev-server_1 ... done
Attaching to hcv_pki_vault-dev-server_1
vault-dev-server_1  | ==> Vault server configuration:
vault-dev-server_1  |
vault-dev-server_1  |              Api Address: http://0.0.0.0:8200
vault-dev-server_1  |                      Cgo: disabled
vault-dev-server_1  |          Cluster Address: https://0.0.0.0:8201
vault-dev-server_1  |               Listener 1: tcp (addr: "0.0.0.0:8200", ...
vault-dev-server_1  |                Log Level: info
vault-dev-server_1  |                    Mlock: supported: true, enabled: false
vault-dev-server_1  |            Recovery Mode: false
vault-dev-server_1  |                  Storage: inmem
vault-dev-server_1  |                  Version: Vault v1.3.1
...
```

---

## Enable PKI plugin

``` txt
# we create the following alias to invoke the vault tool inside the container
$ alias vault="docker-compose exec vault-dev-server vault"

# auth with vault, same password as previous sections
$ vault login

# Enable the pki plugin in the path switches_pki/...
$ vault secrets enable -path=switches_pki pki

# some config
$ vault secrets tune -max-lease-ttl=87600h switches_pki

$ vault write switches_pki/config/urls \
	issuing_certificates="http://127.0.0.1:8200/v1/switches_pki/ca" \
	crl_distribution_points="http://127.0.0.1:8200/v1/switches_pki/crl"
```

---

## Importing the CA certificate

In order to generate certificates we will need a CA certificate to sign them. We can either generate our own certificate and install them in our client machines or we can create an intermediate CA off another CA or intermediate CA.

To simplify things there is an already created self-signed CA in the folder `./ca.`. We can add it to vault as follows:

``` txt
$ vault write switches_pki/config/ca pem_bundle=@/ca/root_bundle.pem
Success! Data written to: switches_pki/config/ca
```

---

# PKI Role

Now we need to create one or more PKI roles. Roles define parameters like domains supported, maximum TTL for the certificates, etc.:

``` txt
$ vault write switches_pki/roles/network-acme-com \
        allowed_domains="network.acme.com" \
        allow_subdomains=true \
        max_ttl="17520h" # 2 years
Success! Data written to: switches_pki/roles/network-acme-com
```

---

# Generating cetificates

``` txt
$ vault write switches_pki/issue/network-acme-com common_name="rtr00.bma.network.acme.com"
Key                 Value
---                 -----
certificate         -----BEGIN CERTIFICATE-----
MIIEkjCCAnqgAwIBAgIUW/M4eFCs5LFA6smJrRlT2H8KqtUwDQYJKoZIhvcNAQEL
...

expiration          1581611003
issuing_ca          -----BEGIN CERTIFICATE-----
MIIFazCCA1OgAwIBAgIUA29vZkyJcXTOeWnmtD1FwVK44SQwDQYJKoZIhvcNAQEL
...

private_key         -----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAmtaw8eHgom1zB39PJj0Yx1NUnaDONbLSdFHlrvUJV2+fQ5Co
...

private_key_type    rsa
serial_number       15-32-65-89-7b-f9-29-86-57-13-6e-c4-c1-1e-9b-e6-5e-d4-d1-9f
```

---

## Listing certificates

``` txt
$ vault list switches_pki/certs
Keys
----
15-32-65-89-7b-f9-29-86-57-13-6e-c4-c1-1e-9b-e6-5e-d4-d1-9f
5b-f3-38-78-50-ac-e4-b1-40-ea-c9-89-ad-19-53-d8-7f-0a-aa-d5
```

---

## Decoding certificates

``` txt
$ vault read switches_pki/cert/30-23-ce-9d-e2-a2-57-4a-2e-44-63-54-c9-15-3d-c5-a0-b0-68-ed \
	-format=json \
		| jq -r ".data.certificate" \
		| openssl x509 -text -noout
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number:
            30:23:ce:9d:e2:a2:57:4a:2e:44:63:54:c9:15:3d:c5:a0:b0:68:ed
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: C = AU, ST = Some-State, O = Internet Widgits Pty Ltd
        Validity
            Not Before: Jan 12 16:25:07 2020 GMT
            Not After : Feb 13 16:25:37 2020 GMT
        Subject: CN = rtr01.bma.network.acme.com
        Subject Public Key Info:
...
```

---

## Revoke certificates

``` txt
vault write switches_pki/revoke \
	serial_number=15-32-65-89-7b-f9-29-86-57-13-6e-c4-c1-1e-9b-e6-5e-d4-d1-9f
Key                        Value
---                        -----
revocation_time            1578847049
revocation_time_rfc3339    2020-01-12T16:37:29.336790549Z
```

---

## Verify CRL

``` txt
$ curl -sS http://127.0.0.1:8200/v1/switches_pki/crl/pem \
	| openssl crl -inform PEM -text -noout
Certificate Revocation List (CRL):
        Version 2 (0x1)
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: C = AU, ST = Some-State, O = Internet Widgits Pty Ltd
        Last Update: Jan 12 17:22:05 2020 GMT
        Next Update: Jan 15 17:22:05 2020 GMT
        CRL extensions:
            X509v3 Authority Key Identifier:
                keyid:48:8D:C9:56:33:AD:44:CD:51:55:D5:B2:27:F8:5B:15:62:CB:A6:6E

Revoked Certificates:
    Serial Number: 153265897BF9298657136EC4C11E9BE65ED4D19F
        Revocation Date: Jan 12 17:22:05 2020 GMT
    Signature Algorithm: sha256WithRSAEncryption
         36:51:1e:55:f1:91:e7:51:25:0c:4b:48:ea:ec:b7:e8:8c:d4:
...
```

---

## Generating cetificates programmatically

``` python
def gen_cert(common_name):
    client = hvac.Client()
    client.token = os.getenv("HCV_TOKEN")

    resp = client.secrets.pki.generate_certificate(
        mount_point="switches_pki",   # path
        name="network-acme-com",      # role
        common_name=f"{common_name}.network.acme.com",
    )
    sn = resp.json()["data"]["serial_number"]
    key = resp.json()["data"]["private_key"]
    crt = resp.json()["data"]["certificate"]

    print(f"{common_name}.network.acme.com: {sn}")

    with open(f"certs/{common_name}.crt", "w+") as f:
        f.write(crt)  # save the cert
    with open(f"certs/{common_name}.key", "w+") as f:
        f.write(key)  # save the key


```

{{<box class="bs-callout bs-callout-info">}}
Full example can be found in <code>cert_gen.py</code>
{{</box>}}

---

## What can I do with this?

1. Integrate with ZTP to provision certificates
2. Use two CAs to provide mTLS authentication
3. Stop ignoring certificate warnings!

{{<box class="bs-callout bs-callout-info">}}
Note that vault has a similar plugin to manage <strong>ssh keys</strong>
{{</box>}}


{{% /section %}}


