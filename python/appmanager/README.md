
#Appmanager
---
## Feature:

Executing shell command on specific host,and you can download and upload file from remote host to local host. 

## PACKAGE:


```
git clone http://10.1.236.106/BDT_FDC/ocdf-back.git
cd appmanager
make
```

## INSTALL:

    yum install ./appmanager-1.0-1.x86_64.rpm

## UNINSTALL: 

    yum remove appmanager



# REST API (Port: 5000)


## 1 '/run' GET
### Feature： run the command line on the specific host

#### normal curl command line

    curl http://127.0.0.1:5000/run?cmd="ls"

#### result:

    Jianhaos-MacBook-Pro:~ jianhaohou$ curl http://127.0.0.1:5000/run?cmd="ls"
    heketi-ha.sh
    main.py
    rest.py
    rest.pyc

#### if command line include  space character， it should use %20 instead

    curl http://127.0.0.1:5000/run?cmd="df%20-h"

#### result:

    Jianhaos-MacBook-Pro:~ jianhaohou$ curl http://127.0.0.1:5000/run?cmd="df%20-h"
    Filesystem      Size   Used  Avail Capacity iused      ifree %iused  Mounted on
    /dev/disk1s5   466Gi   10Gi  388Gi     3%  481738 4881971142    0%   /
    devfs          193Ki  193Ki    0Bi   100%     667          0  100%   /dev
    /dev/disk1s1   466Gi   66Gi  388Gi    15%  588035 4881864845    0%   /System/Volumes/Data
    /dev/disk1s4   466Gi  1.0Gi  388Gi     1%       1 4882452879    0%   /private/var/vm
    map auto_home    0Bi    0Bi    0Bi   100%       0          0  100%   /System/Volumes/Data/home

### 2 '/upload' POST
#### Feature: upload file to specific host from local

        curl -F "file=@/Users/jianhaohou/Documents/1.txt" -F "dest_dir=/Users/jianhaohou/Documents/virtual_folder" -X POST "http://127.0.0.1:5000/upload" -v

### 3 '/download' GET
#### Feature: download file from specific host to local 

    curl http://127.0.0.1:5000/download?file="/Users/jianhaohou/Documents/1.txt" -o "/Users/jianhaohou/3.txt" --progress -v
