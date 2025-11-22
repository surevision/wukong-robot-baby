# -*- coding: utf-8 -*-
# author: wzpan
# 回声

import logging
import re
from robot.sdk.AbstractPlugin import AbstractPlugin

logger = logging.getLogger(__name__)


class Plugin(AbstractPlugin):
    SLUG = "echo"
    PRIORITY = -999
    
    def handle(self, text, parsed):
        text = text.lower().replace("echo", "").replace("传话", "")
        text = re.sub("^说", "", text)
        self.say(text, cache=False)

    def isValid(self, text, parsed):
        return any(word in text.lower() for word in ["echo", "传话"]) or re.match(r"^说.*", text)
