import json
import logging
import time
from datetime import datetime
from config import settings
from elasticsearch import Elasticsearch
import pytz

tz = pytz.timezone(settings.TIME_ZONE)



class LogSender:
    def __init__(self, es):
        self.es = es
        
    def writeLog(self, msg: logging.LogRecord, formatter):
        index_name = f'log_date{time.strftime("%Y_%m_%d")}'
        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        log_data = json.loads(formatter(msg))
        log_data['timestamp'] = timestamp

        self.es.index(index=index_name, document=log_data)