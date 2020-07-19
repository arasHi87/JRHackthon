# ShArKsHaRk

[demo url] (https://www.youtube.com/watch?v=SYgD_tF1Dok)

## Install

first got to root

> cd hackton

install web requirement

建議將 api url 以 ngrok 對外公開，否則前端會因為同源政策無法讀取 api

```sh
$ export SHARK_API_URL=<your api url>
$ cd laradock
$ cp env-example .env
$ docker-compose up -d mysql workspace apache2
$ docker-compose exec workplace bash
$ cd sharkAPI
$ php artisan optimize && php artisan db:seed

$ cd ../sharkWeb
$ npm i && npm run && npm install && npm run build && npm run export
$ mv dist/* ../sharkAPI/public/
```

install crawler requirement

更新資料用，可不做

```sh
$ pip3 install -r requirement.txt
$ cd scrapy crawl StoreGet
```

install bot requirement

需自行申請 line bot 帳號獲得 token 與 secret，並於環境變數中設置
api url 理論上會是 http://localhost/api

```
export ACCESS_TOKEN=<your access token>
export SECRET=<your secret>
export SHARK_API_URL=<the api url>
cd sharkBot
pip3 install requirements.txt
python3 main.py

```
