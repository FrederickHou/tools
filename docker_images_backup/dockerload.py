import os
import sys

if __name__ == "__main__":

    workdir = "/var/lib/docker/image_bak/"
    os.chdir(workdir)
    files = os.listdir(workdir)
    for filename in files:
        print(filename)
        os.system('docker load -i %s'%filename)