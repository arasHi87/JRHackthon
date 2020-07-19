from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from logger import logger
from update import update
from GetShops import GetShops
import yaml,json,os,requests,datetime

if os.getenv('SHARK_API_URL'):
    URL = os.getenv('SHARK_API_URL')
else:
    URL = 'https://5fda577ebdb9.ngrok.io/api'

app = Flask(__name__)
# LINE BOT info
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
SECRET = os.getenv('SECRET')

line_bot_api = LineBotApi(config['ACCESS_TOKEN'])
handler = WebhookHandler(config['SECRET'])

#star links
FullStar = 'https://maps.gstatic.com/consumer/images/icons/2x/ic_star_rate_14.png'
HalfStar = 'https://maps.gstatic.com/consumer/images/icons/2x/ic_star_rate_half_14.png'
EmptyStar = 'https://maps.gstatic.com/consumer/images/icons/2x/ic_star_rate_empty_14.png'

LastUpdateTime = datetime.datetime.now()
MainFolder = str(os.getcwd())
JsonFolder = MainFolder + '/JsonFile/'

def update_Flex(FlexMessage,image, name, address, rating, latitude, longitude):
    #update image
    FlexMessage['hero']['url'] = image
    #update name
    FlexMessage['body']['contents'][0]['text'] = name
    #update star1
    tmp=rating
    for i in range(5):
        if(tmp >= 0.89):
            FlexMessage['body']['contents'][1]['contents'][i]['url'] = FullStar
            tmp -= 1.0
        elif(tmp >= 0.5):
            FlexMessage['body']['contents'][1]['contents'][i]['url'] = HalfStar
            tmp -= 1.0
        else:
            FlexMessage['body']['contents'][1]['contents'][i]['url'] = EmptyStar
    if(rating == 0):
        FlexMessage['body']['contents'][1]['contents'][5]['text'] = 'unrated'
    else:
        FlexMessage['body']['contents'][1]['contents'][5]['text'] = str(float(rating))
    #update address
    FlexMessage['body']['contents'][2]['contents'][0]['contents'][1]['text'] = address
    #update action data in footer
    FlexMessage['footer']['contents'][0]['action']['data'] = '{},{},{},{}'.format(name, address, str(latitude), str(longitude))
    return FlexMessage

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print(body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# Message event
@handler.add(MessageEvent)
def handle_message(event):
    #get message event
    message = event.message
    message_type = message.type
    user_id = event.source.user_id
    reply_token = event.reply_token

    logger.info('UserID: ' + user_id)
    logger.info('MessageType: ' + message_type)
    
    if(update(LastUpdateTime) == 'Failed'):
        line_bot_api.reply_message(reply_token, TextSendMessage(text = 'System Failed'))
        return
    #single search
    if(message_type == 'text'):
        address = message.text
        FlexMessage = json.load(open(JsonFolder + 'FlexMessageTemplate.json','r',encoding='utf-8'))
        Data = json.load(open(JsonFolder + 'Data.json',encoding='utf-8'))
        title = 'res: '
        found = False
        for data in Data:
            if(data['address'].replace(' ','').replace('(△)','').split(',')[0] == address):
                image = data['image']
                name = data['name']
                address = data['address']
                rating = data['rating']
                latitude = data['latitude']
                longitude = data['longitude']
                title += (name + '\n')
                logger.info('Get Data Successfully')
                FlexMessage = update_Flex(FlexMessage,image, name, address, rating, latitude, longitude)
                found = True
                break
        if(not found):
            logger.warning('Data Not Found')
        line_bot_api.reply_message(reply_token, FlexSendMessage(title,FlexMessage))
    #multiple search
    elif(message_type == 'location'):
        CarouselFlexMessage = json.load(open(JsonFolder + 'CarouselFlexMessageTemplate.json','r',encoding='utf-8'))
        FlexMessage = json.load(open(JsonFolder + 'FlexMessageTemplate.json','r',encoding='utf-8'))
        Data = GetShops(event)
        title = ' '
        if(Data):
            for data in Data:
                FlexMessage = json.load(open(JsonFolder + 'FlexMessageTemplate.json','r',encoding='utf-8'))
                image = data['image']
                name = data['name']
                address = data['address']
                rating = data['rating']
                latitude = data['latitude']
                longitude = data['longitude']
                title += (name + '\n')
                logger.info('Get Data Successfully')
                FlexMessage = update_Flex(FlexMessage,image, name, address, rating, latitude, longitude)
                CarouselFlexMessage['contents'].append(FlexMessage)
        else:
            logger.warning('Data Not Found')
            CarouselFlexMessage['contents'].append(FlexMessage)
        line_bot_api.reply_message(reply_token, FlexSendMessage(title,CarouselFlexMessage))
    else:
        line_bot_api.reply_message(reply_token, TextSendMessage(text = '測試成功'))

#PostbackEvent
@handler.add(PostbackEvent)
def handle_postback(event):
    data = event.postback.data.split(',')
    name = data[0]
    address = data[1]
    latitude = data[2]
    longitude = data[3]
    logger.info('PostbackEvent: name: {}\naddress: {}\nlatitude: {}\nlongitude: {}\n'.format(name, address, latitude, longitude))
    line_bot_api.reply_message(event.reply_token, LocationSendMessage(
        title = name,
        address = address,
        latitude = latitude,
        longitude = longitude
    ))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 80))
    app.run(host='0.0.0.0', port=port)