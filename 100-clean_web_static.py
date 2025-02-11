#!/usr/bin/python3
# Delete outdate archives using Fabfile
import os
from fabric.api import *

env.hosts = ['100.26.168.142', '100.25.35.218']


def do_clean(number=0):
    """Delete outdate archives
    Args:
        number (int): The number of archives to keep

    If number is 0 or 1, Keeps only the most recent archive
    if number is 2
    """
    number = 1 if int(number) == 0 else int(number)

    archives = sorted(os.listdir("versions"))
    [archives.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(a)) for a in archives]

    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [a for a in archives if "web_static_" in a]
        [archives.pop() for i in range(number)]
        [run("rm -rf ./{}".format(a)) for a in archives]
