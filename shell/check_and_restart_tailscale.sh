#!/bin/bash
ProcNumber=$(ps -ef | grep -w tailscaled | wc -l)
if [ ${ProcNumber} -le 1 ]; then
echo "no tailscale process, try start"
sudo systemctl stop tailscaled
sudo systemctl start tailscaled
sudo tailscale up
echo "tailscale start called"
else
echo "tailscale already online"
fi

