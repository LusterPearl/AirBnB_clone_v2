#!/usr/bin/python3
"""
Script to deploy the web static
"""

from datetime import datetime
from fabric.api import local, env, run, put
import os

env.hosts = ['100.26.168.142', '100.25.35.218']
env.user = 'ubuntu'
env.key_filename = 'private_key.txt'


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder
    """
    try:
        """ Create the version folder if it doesn't exist """
        if not os.path.exists("versions"):
            local("mkdir -p versions")

        """ Create the archive filename """
        now = datetime.now()
        archive_name = "web_static_{}{}{}{}{}{}.tgz".format(
            now.year, now.month, now.day, now.hour, now.minute, now.second)

        """ Compress the contents of the web_static folder """
        local("tar -cvzf versions/{} web_static".format(archive_name))

        """ Return the archive path if generated successfully """
        return "versions/{}".format(archive_name)

    except Exception as e:
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers
    """
    if not os.path.exists(archive_path):
        return False

    try:
        """ Upload the archive to the /tmp/ directory of the web server """
        put(archive_path, "/tmp/")

        """ Extract the archive to the folder """
        archive_filename = archive_path.split("/")[-1].split(".")[0]
        run("mkdir -p /data/web_static/releases/{}/".format(archive_filename))
        run("tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/"
            .format(archive_filename, archive_filename))

        """ Delete the archive from the web server """
        run("rm /tmp/{}.tgz".format(archive_filename))

        """ Move the contents to the proper location """
        run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/"
            .format(archive_filename, archive_filename))

        """ Remove unnecessary directory """
        run("rm -rf /data/web_static/releases/{}/web_static"
            .format(archive_filename))

        """ Delete the symbolic link /data/web_static/current from the web """
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
            .format(archive_filename))

        print("New version deployed!")

        return True

    except Exception as e:
        return False


def deploy():
    """
    Deploy the web static
    """
    """ Call do_pack() and store archive path """
    archive_path = do_pack()

    """ Return False if no archive has been created """
    if archive_path is None:
        return False

    """ Call do_deploy(archive_path) """
    result = do_deploy(archive_path)

    """ Return the result of do_deploy """
    return result


"""Run the deploy() function when script is executed"""
if __name__ == "__main__":
    deploy()
