
# -*- coding:utf-8 -*-
import os
import json
import requests
import time
from robot import logging

logger = logging.getLogger(__name__)
class paddleSpeech(object):
    def __init__(self, asr_url, model_dir=''):
        self.asr_url = asr_url
        self.model_dir = model_dir

    def asr(self, file):
        asr_url = self.asr_url
        files = {'files': open(file, 'rb')}
        try:
            response = requests.post(asr_url, files=files)
            print(response.text)
            s = response.content.decode("utf-8")
            return json.loads(s)
        except Exception as err:
            logger.error(f"paddlespeech error: {err}", stack_info=True)