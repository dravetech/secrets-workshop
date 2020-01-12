#!/usr/bin/env python
import os
import sys

import hvac


def gen_cert(common_name):
    client = hvac.Client()
    client.token = os.getenv("HCV_TOKEN")

    resp = client.secrets.pki.generate_certificate(
        mount_point="switches_pki",
        name="network-acme-com",
        common_name=f"{common_name}.network.acme.com",
    )
    sn = resp.json()["data"]["serial_number"]
    key = resp.json()["data"]["private_key"]
    crt = resp.json()["data"]["certificate"]

    print(f"{common_name}.network.acme.com: {sn}")

    with open(f"certs/{common_name}.crt", "w+") as f:
        f.write(crt)
    with open(f"certs/{common_name}.key", "w+") as f:
        f.write(key)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(f"Usage: {sys.argv[0]} CN_1 [CN_2] ... [CN_3]")
        sys.exit(1)

    for cn in sys.argv[1:]:
        gen_cert(cn)
