echo "Leprechaun B installing."
sudo groupadd -g 7979 leprechaunb
sudo useradd -m -u 7979 -g 7979 leprechaunb
PY_SITE=$(python3 -c "import site; print(site.getsitepackages()[0])")
echo Python3 Site: ${PY_SITE}
sudo mkdir -p ${PY_SITE}
sudo su -c "pwd > ${PY_SITE}/leprechaunb.pth"
sudo cp rt/rt.service /etc/systemd/system/
sudo cp ts/ts.service /etc/systemd/system/
sudo cp arrows/arrows.service /etc/systemd/system/
sudo cp wap/wap.service /etc/systemd/system/
sudo cp nginx/leprechaunb /etc/nginx/sites-enabled/leprechaunb
sudo systemctl restart nginx
sudo nginx -s reload
sudo systemctl daemon-reload
sudo systemctl start rt
sudo systemctl start ts
sudo systemctl start arrows
sudo systemctl start wap
sudo systemctl enable rt
sudo systemctl enable ts
sudo systemctl enable arrows
sudo systemctl enable wap
ps aux | grep leprechaunb/leprechaunb | grep -v grep
echo "Leprechaun B installed."
