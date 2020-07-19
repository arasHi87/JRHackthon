import requests,json,datetime,os,codecs
from logger import logger
CycleLength = datetime.timedelta(hours=1)
MainFolder = str(os.getcwd())
JsonFolder = MainFolder + '/JsonFile/'

URL = os.getenv('SHARK_API_URL', 'https://5fda577ebdb9.ngrok.io') + '/api/store'

def update(LastUpdateTime):
    NowTime = datetime.datetime.now()
    logger.info('LastUpdateTime: {}\nNowTime: {}'.format(LastUpdateTime,NowTime))
    if(NowTime-LastUpdateTime >= CycleLength):
        logger.info('====================Downloading====================')
        try:
            Data = requests.get(URL)
            logger.info('Request Successfully')
        except:
            logger.error('Request Failed')
            return 'Failed'
        try:
            contents = Data.json()
            with open(JsonFolder + 'Data.json','w',encoding='utf-8') as f:
                json.dump(contents, f, ensure_ascii=False,indent=4)
            logger.info('===============Download Successfully===============')
            return 'Success'
        except Exception as err:
            print(err)
            logger.error('Open Data.json Failed')
            logger.info('==================Download Failed==================')
            return 'Failed'