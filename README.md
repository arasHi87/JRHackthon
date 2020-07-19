# ShArKsHaRk

## Install

first got to root

> cd hackton

install web requirement

```sh
$ cd laradock
$ cp env-example .env
$ docker-compose up -d mysql workspace apache2

$ cd ../sharkWeb
$ npm i && npm run && npm install && npm run build && npm run export
$ mv dist/* ../sharkAPI/public/
$ cd ../sharkAPI
$ php artisan db:seed
$ php artisan optimize
```

install crawler requirement

更新資料用，可不做

```sh
$ pip3 install -r requirement.txt
$ cd scrapy crawl StoreGet
```

install bot requirement

需自行申請 line bot 帳號獲得 token 與 secret，並於環境變數中設置

```
export ACCESS_TOKEN=<your access token>
export SECRET=<your secret>
cd sharkBot
pip3 install requirements.txt
python3 main.py

```
