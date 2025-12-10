sudo chmod +x /home/admin/shell/startup.sh
sudo chmod 644 /lib/systemd/system/mystartup.service
sudo systemctl daemon-reload
sudo systemctl enable mystartup.service
sudo systemctl start mystartup.service