---
---

{{% section %}}

1. {{< greyed c="Introduction" >}}
1. {{< greyed c="Do's and Dont's" >}}
1. {{< notgreyed c="Intro to GnuPG" >}}
1. {{< greyed c="Encrypted Environment" >}}
1. {{< greyed c="Encrypted Inventory" >}}
1. {{< greyed c="Hashicorp Vault 101" >}}
1. {{< greyed c="Storing secrets in HCV" >}}
1. {{< greyed c="Building a PKI with HCV" >}}
1. {{< greyed c="Summary" >}}

---

# Intro to GnuPG

{{<box class="bs-callout bs-callout-quote">}}
 <a href="https://gnupg.org/">GnuPG</a> is a complete and free implementation of the OpenPGP standard as defined by RFC4880 (also known as PGP). GnuPG allows you to encrypt and sign your data and communications; it features a versatile key management system, along with access modules for all kinds of public key directories. GnuPG, also known as GPG, is a command line tool with features for easy integration with other applications. A wealth of frontend applications and libraries are available. GnuPG also provides support for S/MIME and Secure Shell (ssh).
{{</box>}}

In this section we are going to see how to use it to encrypt a decrypt files with `GnuPG`

{{<box class="bs-callout bs-callout-info">}}
Files for this section can be found in the folder <code>./code/gpg/</code>
{{</box>}}

---

## Encrypting files

File in clear-text:

``` txt
$ cat unencrypted.txt
This is text we want to secure
```

Encrypting the file:

``` txt
$ gpg --symmetric -o unencrypted.txt.gpg unencrypted.txt

$ file unencrypted.txt.gpg
unencrypted.txt.gpg: GPG symmetrically encrypted data (AES cipher)
```
---

## Decrypting files

``` txt
$ gpg --decrypt -o unencrypted.txt unencrypted.txt.gpg
gpg: AES encrypted data
gpg: encrypted with 1 passphrase
```


{{<box class="bs-callout bs-callout-info">}}
Password in the example file is <code>apassword</code>
{{</box>}}

---

## More about GnuPG

* Smartcards
* Asymmetric encryption

{{% /section %}}
