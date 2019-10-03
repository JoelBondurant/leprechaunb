echo "Leprechaun B installing."
sudo groupadd -g 7979 leprechaunb
sudo useradd -m -u 7979 -g 7979 leprechaunb
PY_SITES=$(python3 -c "import site; print(site.getsitepackages()[0])")
echo Python3 Sites: ${PY_SITES}
mkdir -p ${PY_SITES}
pwd > ${PY_SITES}/leprechaunb.pth
sudo cp arrows/rt.service /etc/systemd/system/
sudo cp arrows/ts.service /etc/systemd/system/
sudo cp arrows/arrows.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable rt
sudo systemctl enable ts
sudo systemctl enable arrows
echo "Leprechaun B installed."
