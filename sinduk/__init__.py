import os
from os.path import basename
import johnnycanencrypt as jce
import argparse
import getpass


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
    filename = os.path.join(dirname,resource_name)
    # checking if the resource_name has `/` in it
    if resource_name.find("/"):
        dirname = os.path.join(dirname, os.path.dirname(resource_name))
        # https://docs.python.org/3/library/os.html#os.makedirs 
        # if the directory exists do not throw any error
        os.makedirs(dirname, 0o700, True)
        
    
    with open(filename,"w") as fobj:
        # TODO: encrypt the password
        fobj.write(password)
    print(f"Password successfully saved under {resource_name}.")
    


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--init", help="pass the OpenPGP key file ", type=str)
    parser.add_argument("--insert", help="pass the resource name", type=str)
    args = parser.parse_args()
    if args.init:
        init(args.init)
    elif args.insert:
        insert(args.insert)



    
    