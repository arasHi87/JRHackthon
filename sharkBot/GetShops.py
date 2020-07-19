import json,os
from logger import logger
from GetDistance import distance
MainFolder = str(os.getcwd())
JsonFolder = MainFolder + '/JsonFile/'

def GetShops(event):
    if(event.message.type == 'location'):
        try:
            positions = open(JsonFolder + 'Data.json','r',encoding='utf-8')
            logger.info('open Data.json Successfully')
        except:
            logger.warning('open Data.json Failed')
        radius = 1.0 #km
        result = []
        StoreData = json.load(positions)
        lat1 = float(event.message.latitude)
        lng1 = float(event.message.longitude)
        result = sorted(StoreData, key=lambda x: (distance(lat1, lng1, float(x['latitude']), float(x['longitude']))))
        return result[:10] # 10 maximun