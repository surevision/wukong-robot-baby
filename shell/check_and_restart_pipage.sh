#!/bin/bash
cd /home/admin

export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init - bash)"
eval "$(pyenv virtualenv-init -)"

export PYTHON_BUILD_MIRROR_URL="https://registry.npmmirror.com/-/binary/python"
export PYTHON_BUILD_MIRROR_URL_SKIP_CHECKSUM=1

cd /home/admin/shell
bash check_and_restart_wukong.sh

ProcNumber=$(ps -ef | grep -w page_server | wc -l)
if [ ${ProcNumber} -le 1 ]; then
echo "no page_server process, try start"
cd /home/admin/pi-page
nohup python page_server.py &
else
echo "tailscale already online"
fi
sleep 1s
chromium-browser --incognito --kiosk "http://localhost:6001"