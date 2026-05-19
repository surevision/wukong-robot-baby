#!/bin/bash

cd /home/pi

#export PYENV_ROOT="$HOME/.pyenv"
#[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
#eval "$(pyenv init - bash)"
#eval "$(pyenv virtualenv-init -)"

export PYTHON_BUILD_MIRROR_URL="https://registry.npmmirror.com/-/binary/python"
export PYTHON_BUILD_MIRROR_URL_SKIP_CHECKSUM=1

ProcNumber=`ps -ef | grep -w wukong.py | grep -v grep | wc -l`
echo ${ProcNumber}
if [ ${ProcNumber} -le 1 ]; then
echo "no wukong process, try start"
cd /home/pi
cd /home/pi/wukong-robot
nohup /usr/bin/python wukong.py &
echo "wukong start called"
else
echo "wukong already online"
fi

