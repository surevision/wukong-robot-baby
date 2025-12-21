# -*- coding: utf-8-*-

import os
import datetime
from robot import constants, utils
from robot.sdk.AbstractPlugin import AbstractPlugin

from robot import config, logging

logger = logging.getLogger(__name__)

class Plugin(AbstractPlugin):

    SLUG = "foodtime"

    def handle(self, text, parsed):
        # 获取当前时间
        now = datetime.datetime.now()
        formatted_date = now.strftime("%Y年%m月%d日")
        formatted_time = now.strftime("%H点%M分")
        if u"记吃奶时间" in text or u"记录吃奶时间" in text or u"记下吃奶时间" in text or u"记一下吃奶时间" in text:
            path = config.get("/foodtime/path")
            with open(os.path.join(path, formatted_date), "w+") as f:
                f.write(f"{formatted_time}\n")
            self.say(f"已记录本次吃奶时间 {formatted_time}", cache=False)
        elif u"上次吃奶时间" in text:
            path = config.get("/foodtime/path")
            filename = os.path.join(path, formatted_date)
            if os.path.exists(filename):
                with open(filename, "r") as f:
                    times = f.readlines()
                    if len(times) <= 0:
                        self.say(f"今天还没有记录过吃奶时间", cache=True)
                    else:
                        timestr = times[-1]
                        self.say(f"上次吃奶时间是 {timestr}", cache=False)
            else:
                self.say(f"今天还没有记录过吃奶时间", cache=True)
        elif u"今天吃奶时间" in text:
            path = config.get("/foodtime/path")
            filename = os.path.join(path, formatted_date)
            if os.path.exists(filename):
                with open(filename, "r") as f:
                    times = f.readlines()
                    if len(times) <= 0:
                        self.say(f"今天还没有记录过吃奶时间", cache=True)
                    else:
                        self.say(f"今天吃奶时间为", cache=True)
                        for timestr in times:
                            self.say(f"{timestr}", cache=False)
            else:
                self.say(f"今天还没有记录过吃奶时间", cache=True)
        elif u"昨天吃奶时间" in text:
            day = datetime.datetime.now() - datetime.timedelta(days=1)
            formatted_date = day.strftime("%Y年%m月%d日")
            path = config.get("/foodtime/path")
            filename = os.path.join(path, formatted_date)
            if os.path.exists(filename):
                with open(filename, "r") as f:
                    times = f.readlines()
                    if len(times) <= 0:
                        self.say(f"昨天没有记录过吃奶时间", cache=True)
                    else:
                        self.say(f"昨天吃奶时间为", cache=True)
                        for timestr in times:
                            self.say(f"{timestr}", cache=False)
            else:
                self.say(f"昨天没有记录过吃奶时间", cache=True)
        elif u"前天吃奶时间" in text:
            day = datetime.datetime.now() - datetime.timedelta(days=2)
            formatted_date = day.strftime("%Y年%m月%d日")
            path = config.get("/foodtime/path")
            filename = os.path.join(path, formatted_date)
            if os.path.exists(filename):
                with open(filename, "r") as f:
                    times = f.readlines()
                    if len(times) <= 0:
                        self.say(f"前天没有记录过吃奶时间", cache=True)
                    else:
                        self.say(f"前天吃奶时间为", cache=True)
                        for timestr in times:
                            self.say(f"{timestr}", cache=False)
            else:
                self.say(f"前天没有记录过吃奶时间", cache=True)

    def isValid(self, text, parsed):
        return any(word in text.lower() for word in [u"记吃奶时间", u"记录吃奶时间", u"记下吃奶时间", u"记一下吃奶时间", u"今天吃奶时间", u"昨天吃奶时间", u"前天吃奶时间", u"上次吃奶时间"])