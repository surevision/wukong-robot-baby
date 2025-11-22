# -*- coding: utf-8-*-

import os
import datetime
from robot import constants, utils
from robot.sdk.AbstractPlugin import AbstractPlugin

class Plugin(AbstractPlugin):

    SLUG = "calander"

    def handle(self, text, parsed):
        # 获取当前时间
        now = datetime.datetime.now()

        # 格式化时间字符串
        formatted_time = now.strftime("%Y年%m月%d日 %H点%M分")
        self.say(formatted_time, cache=True)

    def isValid(self, text, parsed):
        return any(word in text.lower() for word in ["几点啦", u"几点了", u"现在时间"])