APP_ROOT="$(dirname "$(dirname "$(readlink -fm "$0")")")"
cd $APP_ROOT

virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
