echo "Leprechaunb installing."
PY_USER_SITES=$(python3 -m site --user-site)
echo Python3 User Sites: ${PY_USER_SITES}
mkdir -p ${PY_USER_SITES}
echo $PWD > ${PY_USER_SITES}/leprechaunb.pth
echo "Leprechaunb installed."
