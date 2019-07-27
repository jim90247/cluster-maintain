#!/bin/bash
set -xe
git clone https://github.com/cea-hpc/modules.git
cd modules
./configure --prefix=/opt/Modules --modulefilesdir=/opt/modulefiles
make
make install
clush -a 'echo "source /opt/Modules/init/profile.sh" >> /etc/zshenv'
clush -a 'echo "source /opt/Modules/init/profile.sh" >> /etc/bashrc'
