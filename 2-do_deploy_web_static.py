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
env.key_filename = 'my_ssh_private_key.txt'


def do_deploy(archive_path):
    """Deploys archive to webservers"""
    if os.path.exists(archive_path):
        try:

            # Extract the filename without extension
            fileName = os.path.splitext(os.path.basename(archive_path))[0]

            # Upload the archive to /tmp/ directory on the web server
            put(archive_path, "/tmp/{}.tgz".format(fileName))

            # Create destination directory
            destination = "/data/web_static/releases/{}".format(fileName)
            run("mkdir -p {}".format(destination))

            # Extract the archive to the destination directory
            run("tar -xzf /tmp/{}.tgz -C {}".format(fileName, destination))

            # Remove the archive from /tmp/
            run("rm -rf /tmp/{}.tgz".format(fileName))

            # Remove the symbolic link /data/web_static/current
            run("rm -rf /data/web_static/current")

            # Create a new symbolic link /data/web_static/current
            run("ln -s {}/ /data/web_static/current".format(destination))

            return True
        except Exception as e:
            return False
    else:
        return False
