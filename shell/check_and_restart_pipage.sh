#!/bin/bash
cd /home/pi

#export PYENV_ROOT="$HOME/.pyenv"
#[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
#eval "$(pyenv init - bash)"
#eval "$(pyenv virtualenv-init -)"

export PYTHON_BUILD_MIRROR_URL="https://registry.npmmirror.com/-/binary/python"
export PYTHON_BUILD_MIRROR_URL_SKIP_CHECKSUM=1

# cd /home/pi/shell
# bash check_and_restart_wukong.sh

ProcNumber=$(ps -ef | grep -w page_server | wc -l)
if [ ${ProcNumber} -le 1 ]; then
echo "no page_server process, try start"
cd /home/pi/pi-page
nohup /usr/bin/python page_server.py &
else
echo "page_server already online"
fi
sleep 1s

chromium-browser --incognito --kiosk --disable-features=Translate --password-store=basic "http://localhost:6001"
