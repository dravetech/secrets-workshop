---
---

{{% section %}}

## Maybe

---

### Authentication, Integrity and Privacy

**Authentication** is the act of being able to prove the identity of a person or system

Data has **integrity** if it can be proven it hasn't been manipulated by an unauthorized actor

**Privacy** is the condition of being free from unauthorized observers

---

### Authentication, Integrity and Privacy

If you can't guarantee any of these properties you can't guarantee a system is secure


**TLS** guarantees all three properties, however, if the private key of the certificate is leaked a malicious actor could impersonate the server and perform a MiTM attack (authentication being voided), decrypt user-server communications (privacy being compromised) and even manipulate the HTML code to redirect the user to malicious servers (integrity no longer guaranteed)

---

{{% /section %}}
