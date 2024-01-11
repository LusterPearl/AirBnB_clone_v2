#!/usr/bin/python3
"""
Fabric script (based on the file 1-pack_web_static.py) that distributes
an archive to your web servers
"""
from fabric.api import *
import os
from datetime import datetime

env.hosts = ['100.26.168.142', '100.25.35.218']
env.user = 'ubuntu'
env.key_filename = 'private_key.txt'



