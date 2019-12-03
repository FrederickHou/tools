#coding:utf-8

import re
import os
import subprocess
import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", help ="docker bakup dir")
    args = parser.parse_args()


if __name__ == "__main__":

    if not args.dir:
        print "ERROR: PLEASE INPUT A DOCKER BACKUP DIR ,or imput python main.py -h"
        os.exit(-1)
    os.system('rm -rf /var/lib/docker/image_bak')
    os.system('mkdir -p /var/lib/docker/image_bak')
    p = subprocess.Popen('docker images', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout.readlines():

        # 此处的正则表达式是为了匹配镜像名以docker.io为开头的镜像
        # 实际使用中根据需要自行调整
        m = re.match(r'(^s+)', line.decode("utf-8"))
        if not m:
            continue

        # 镜像名
        iname = m.group(1).strip(' ')
        # tag
        itag = m.group(2)

        # tar包的名字
        tarname = iname.split('/')[-1]
        print(tarname)
        tarball = tarname + '.tar'
        ifull = iname + ':' + itag
        #save
        cmd = 'docker save -o ' + tarball + ' ' + ifull
        os.system(cmd)
        tarname = tarball + ".gz"
        os.system("tar -zcvf %s %s" %(tarball,tarname))
        # 将tar包放在临时目录
        os.system('mv %s /var/lib/docker/image_bak/'%tarname)


    retval = p.wait()
