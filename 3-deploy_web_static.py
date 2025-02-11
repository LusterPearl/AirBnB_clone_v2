#!/usr/bin/python3
"""
Script to deploy the web static
"""

from datetime import datetime
from fabric.api import local, env, run, put
import os

env.hosts = ['100.26.168.142', '100.25.35.218']
env.user = 'ubuntu'
env.key_filename = 'my_ssh_private_key.txt'


def do_pack():
    """create .tgz archive of web_static/ folder"""
    try:
        arch_name = "web_static_{}.tgz".format(
            datetime.now().strftime('%Y%m%d%H%M%S'))
        local("mkdir -p versions/")
        local("tar -cvzf versions/{} -C {} .".format(
            arch_name, "web_static/"))
        return "versions/{}".format(arch_name)
    except Exception as e:
        return None


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


def deploy():
    ''' controls the deployment'''
    archive = do_pack()
    if archive is None:
        return False
    deployment = do_deploy(archive)
    return deployment
