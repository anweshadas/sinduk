import os
from os.path import basename
import johnnycanencrypt as jce

def init():
    "initials the sinduk project for the user"
    dirname = os.path.expanduser("~/.sinduk")
    if os.path.exists(dirname):
        return
    os.mkdir(dirname)
    
    