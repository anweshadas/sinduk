import os
from os.path import basename
import johnnycanencrypt as jce
import argparse


def init(keyfile: str):
    "initials the sinduk project for the user"
    if not os.path.exists(keyfile):
        print("The OpenPGP keyfile does not exist.")
        return
    dirname = os.path.expanduser("~/.sinduk")
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    ks = jce.KeyStore(dirname)
    ks.import_cert(keyfile)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--init", help="pass the OpenPGP key file ", type=str)
    args = parser.parse_args()
    if args.init:
        init(args.init)



    
    