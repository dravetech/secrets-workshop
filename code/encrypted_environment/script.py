#!/usr/bin/env python
import os


if __name__ == "__main__":
    default = os.getenv("DEFAULT_PASSWORD")
    bma = os.getenv("BMA_PASSWORD")

    print(f"DEFAULT_PASSWORD = {default}")
    print(f"BMA_PASSWORD = {bma}")
