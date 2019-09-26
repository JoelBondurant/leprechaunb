echo "wap restarting."
echo "killing flask wap"
pkill flask
echo "starting flask wap"
cd ./wap
export FLASK_APP="wap"
export FLASK_ENV="development"
nohup flask run --host=127.0.0.1 --port=8880 </dev/null >/dev/null 2>&1 &
cd ..
