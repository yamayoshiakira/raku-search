らくサーチ　raku-search.appspot.com

# Terminal 1: datastore emulator
sudo update-alternatives --auto java
export JAVA_TOOL_OPTIONS="-Xmx256m -Xms128m"
gcloud beta emulators datastore start --host-port=0.0.0.0:8081 --project=raku-search
 
# Terminal 2: Flask run
gcloud config set project raku-search
export DATASTORE_EMULATOR_HOST=localhost:8081
cd ~/raku-search/gae
source venv/bin/activate
export FLASK_APP=main.py
export FLASK_DEBUG=1
export FLASK_RUN_HOST=0.0.0.0
export FLASK_RUN_PORT=8080
#flask run --host=0.0.0.0 --port=8080
flask run


# pip install
cd ~/raku-search/gae
source venv/bin/activate
pip3 install -r requirements.txt

---------------------------------------------


# git
git config --global user.name "yamayoshiakira"
git config --global user.email "yamayoshiakira@gmail.com"
git config --list


# Terminal 1: datastore emulator
sudo update-alternatives --auto java
export JAVA_TOOL_OPTIONS="-Xmx256m -Xms128m"
gcloud beta emulators datastore start --host-port=0.0.0.0:8081 --project=raku-search

# Terminal 2: Flask run
export DATASTORE_EMULATOR_HOST=localhost:8081
cd ~/raku-search
source env/bin/activate
cd project
export FLASK_APP=main.py
export FLASK_DEBUG=1
export FLASK_RUN_HOST=0.0.0.0
export FLASK_RUN_PORT=8080
#flask run --host=0.0.0.0 --port=8080
flask run


--------------------------------------------------------

Config.py に、シークレットの取り出しコード書く


Cloud Shell に VS Code で接続する



[Flask 起動] R:$
cd ~/raku-search
source env/bin/activate
cd project
export FLASK_APP=main.py
export FLASK_DEBUG=1
export FLASK_RUN_HOST=0.0.0.0
export FLASK_RUN_PORT=8080
#flask run --host=0.0.0.0 --port=8080
flask run

https://8080-cs-6725a215-f8aa-4cca-97ad-62600315f1f2.cs-asia-east1-duck.cloudshell.dev/test

[Cloud Shell]
L:$ ./start_gcp.sh raku-search

[tmux] ウインドゥ切り替え
R:$ Ctrl+b -> w

[開発環境]
sudo apt update && sudo apt upgrade
cd ~/raku-search
python3 -m venv env
source env/bin/activate
pip3 install -r project/requirements.txt

--------------------------------------------------

[Start Datastore] terminal#1
gcloud beta emulators datastore start

[Start Project] terminal#2
export DATASTORE_EMULATOR_HOST=localhost:8081
export GOOGLE_APPLICATION_CREDENTIALS="/home/yamayoshiakira/raku-search/project/raku-search-804220f74370.json"
export FLASK_ENV=development
cd ~/raku-search && source env/bin/activate && cd project
python3 main.py


[開発環境]
sudo apt update && sudo apt upgrade
mkdir raku-search
cd ~/raku-search
python3 -m venv env
source env/bin/activate
pip3 install -r project/requirements.txt



-------------------------------------------------------

アナリティクス

--
[Start Datastore] terminal#1
gcloud beta emulators datastore start

[Start Project] terminal#2
export DATASTORE_EMULATOR_HOST=localhost:8081
export GOOGLE_APPLICATION_CREDENTIALS="/home/yamayoshiakira/raku-search/project/raku-search-804220f74370.json"
export FLASK_ENV=development
cd ~/raku-search && source env/bin/activate && cd project
python3 main.py

[Deploy]
$ gcloud app deploy --project=raku-tabi --version=3a
$ gcloud app deploy cron.yaml --project=raku-tabi

--
仮想環境 venv
$ sudo apt update && sudo apt upgrade
$ sudo apt install python3-dev python3-venv build-essential
$ cd ~/raku-search
$ python3 -m venv env
$ source ./env/bin/activate
V pip3 install -U pip setuptools
V pip3 install grpcio
V pip3 install Flask requests google-cloud-datastore google-cloud-tasks
V deactivate

アカウントキーの作成
https://cloud.google.com/docs/authentication/production?hl=ja#manually
> raku-search-804220f74370.json


----------------------------------------------------------------
base.html
<script src="/static/custom.js"></script>

dispatch.yaml -> backend
https://cloud.google.com/appengine/docs/standard/python3/reference/dispatch-yaml?hl=ja
https://qiita.com/sinmetal/items/017e7aa395ff459fca7c


らく旅  http://raku-tabi.appspot.com/

python27 -> Python3
Django   -> Flask
task, backend, memcache 等は、一旦Python3でリリースしてから着手

[Start Datastore] terminal#1
gcloud beta emulators datastore start

[Start Project] terminal#2
export DATASTORE_EMULATOR_HOST=localhost:8081
export GOOGLE_APPLICATION_CREDENTIALS="/home/yamayoshiakira/raku-tabi/project/raku-tabi-7ed776199429.json"
export FLASK_ENV=development
cd ~/raku-tabi && source env/bin/activate && cd project
python3 main.py

[Deploy]
$ gcloud app deploy --project=raku-tabi --version=3a

$ gcloud app deploy cron.yaml --project=raku-tabi



仮想環境 venv
$ sudo apt update && sudo apt upgrade
$ sudo apt install python3-dev python3-venv build-essential
$ cd ~/raku-tabi
$ python3 -m venv env
$ source ./env/bin/activate
V pip3 install -U pip setuptools
V pip3 install grpcio
V pip3 install Flask requests google-cloud-datastore google-cloud-tasks

GAE 認証キー
https://console.cloud.google.com/iam-admin/serviceaccounts?folder=&organizationId=&project=raku-tabi&supportedpurview=project


