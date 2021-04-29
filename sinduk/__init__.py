import os
from os.path import basename
import johnnycanencrypt as jce
import argparse
import sys
import getpass
import pathlib
from typing import List
import pyperclip as pc


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


def insert(resource_name: str):
    "take password from the user"
    password = getpass.getpass()
    password1 = getpass.getpass()
    if password != password1:
        print("Both the passwords are not same. Enter the correct password.")
        return

    dirname = os.path.expanduser("~/.sinduk")
    # encrypting the password
    ks = jce.KeyStore(dirname)
    key = ks.get_all_keys()[0]
    enc = ks.encrypt(key, password)

    filename = os.path.join(dirname, resource_name)
    # checking if the resource_name has `/` in it
    if resource_name.find("/"):
        dirname = os.path.join(dirname, os.path.dirname(resource_name))
        # https://docs.python.org/3/library/os.html#os.makedirs
        # if the directory exists do not throw any error
        os.makedirs(dirname, 0o700, True)

    with open(filename, "wb") as fobj:
        fobj.write(enc)
    print(f"Password successfully saved under {resource_name}.")


def show(resource_name: List[str],clipboard: bool):
    accname = resource_name[0].strip()
    dirname = os.path.expanduser("~/.sinduk")
    ks = jce.KeyStore(dirname)
    key = ks.get_all_keys()[0]
    p = pathlib.Path(dirname)
    if not accname:
        for fname in p.glob("**/*"):
            if fname.is_file() and fname.name != "jce.db":
                print(fname)
    else:
        print("Enter the password for Sinduk?")
        password = getpass.getpass()
        filepath = os.path.join(dirname, accname)

        print(filepath)
        with open(filepath, "rb") as fobj:
            enc = fobj.read()
            enctext = ks.decrypt(key, enc, password)
            text = enctext.decode("utf-8")
            if clipboard:
                pc.copy(text)
            else:
                print(text)

            
    

    


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--init", help="pass the OpenPGP key file ", type=str)
    parser.add_argument("--insert", help="pass the resource name", type=str)
    parser.add_argument("-c", help="copy the password in the clipboard", action="store_true")
    parser.add_argument(
        "resource_name",
        metavar="resource_name",
        type=str,
        nargs="*",
        default=[""],
        help="Name of the account",
    )
    args = parser.parse_args()
    if args.init:
        init(args.init)
    elif args.insert:
        insert(args.insert)
    
    else:
        show(args.resource_name, args.c)
