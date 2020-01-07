#!/usr/bin/env python
import os

import hvac
from hvac.exceptions import InvalidPath


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


if __name__ == "__main__":
    print(f"default = {get_password_from_path('defaults')}")
    print(f"bma = {get_password_from_path('bma')}")
    print(f"bma/rtr00 = {get_password_from_path('bma/rtr00')}")
