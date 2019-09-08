echo "Bitcoin Arrows installing."
PY_USER_SITES=$(python3 -m site --user-site)
echo Python3 User Sites: ${PY_USER_SITES}
mkdir -p ${PY_USER_SITES}
echo $PWD > ${PY_USER_SITES}/bitcoinarrows.pth
echo "Bitcoin Arrows installed."
