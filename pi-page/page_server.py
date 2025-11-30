
import os
import uuid
import json
import time
import base64
import random
import signal
import hashlib
import asyncio
import requests
import threading
import subprocess
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver

PORT = "6001"

APP_PATH = os.path.normpath(
    # os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir)
    os.path.dirname(os.path.abspath(__file__))
)


settings = {
    "template_path": os.path.join(APP_PATH, "html"),
    "static_path": os.path.join(APP_PATH, "static"),
    "debug": False,
}

class BaseHandler(tornado.web.RequestHandler):
    def initialize(self, key="", uuid=""):
        self.key = key
        self.uuid = uuid

class MainHandler(BaseHandler):
    def get(self):
        # 取儿歌列表
        song_list = []
        with open(os.path.join(APP_PATH, "static/erge/list.txt"), 'r', encoding='utf-8') as f:
            songs = f.readlines()
            song_list = [song.split("$")[0] for song in songs]
        # 取成语列表
        chengyu_list = []
        with open(os.path.join(APP_PATH, "static/chengyu/list.txt"), 'r', encoding='utf-8') as f:
            chengyus = f.readlines()
            chengyu_list = [chengyu.split("$")[0] for chengyu in chengyus]
        file = "small.html"
        if (self.get_argument("theme", "small") == "big"):
            file = "normal.html"
        self.render(file, song_list=song_list, chengyu_list=chengyu_list)

class ErgeHandler(BaseHandler):
    def post(self):
        post_data = self.request.body_arguments
        print(post_data)
        post_data = {x: post_data.get(x)[0].decode("utf-8") for x in post_data.keys()}
        if not post_data:
            post_data = self.request.body.decode('utf-8')
            post_data = json.loads(post_data)
        control = post_data.get("control", None)
        name = post_data.get("name", None)
        url = f"http://localhost:5001/chat"
        data = {
            "type": "text",
            "uuid": self.uuid,
            "validate": self.key
        }
        query = ""
        if control == "stop":
            query = "停止儿歌"
        else:
            if name is None or name == "":
                # 随机一个
                query = "随便唱一个儿歌"
            else:
                query = f"唱儿歌{name}"
        data["query"] = query
        response = requests.post(url=url, params=data)
        response.raise_for_status()
        print(response.text)

class ChengyuHandler(BaseHandler):
    def post(self):
        post_data = self.request.body_arguments
        print("post_data:-------------------")
        print(post_data)
        post_data = {x: post_data.get(x)[0].decode("utf-8") for x in post_data.keys()}
        if not post_data:
            post_data = self.request.body.decode('utf-8')
            post_data = json.loads(post_data)
        control = post_data.get("control", None)
        name = post_data.get("name", None)
        url = f"http://localhost:5001/chat"
        data = {
            "type": "text",
            "uuid": self.uuid,
            "validate": self.key
        }
        query = ""
        if control == "stop":
            query = "停止成语故事"
        else:
            if name is None or name == "":
                # 随机一个
                query = "随便讲一个成语故事"
            else:
                query = f"讲成语故事{name}"
        data["query"] = query
        response = requests.post(url=url, params=data)
        response.raise_for_status()
        print(response.text)


class WeatherHandler(BaseHandler):
    def post(self):
        post_data = self.request.body_arguments
        print(post_data)
        post_data = {x: post_data.get(x)[0].decode("utf-8") for x in post_data.keys()}
        if not post_data:
            post_data = self.request.body.decode('utf-8')
            post_data = json.loads(post_data)
        control = post_data.get("control", None)
        name = post_data.get("name", None)
        url = f"http://localhost:5001/chat"
        data = {
            "type": "text",
            "uuid": self.uuid,
            "validate": self.key
        }
        query = "天气预报"
        data["query"] = query
        response = requests.post(url=url, params=data)
        response.raise_for_status()
        print(response.text)


class IPCheckHandler(BaseHandler):
    def post(self):
        post_data = self.request.body_arguments
        print(post_data)
        post_data = {x: post_data.get(x)[0].decode("utf-8") for x in post_data.keys()}
        if not post_data:
            post_data = self.request.body.decode('utf-8')
            post_data = json.loads(post_data)
        control = post_data.get("control", None)
        name = post_data.get("name", None)
        url = f"http://localhost:5001/chat"
        data = {
            "type": "text",
            "uuid": self.uuid,
            "validate": self.key
        }
        print(json.dumps(data))
        query = "本地IP"
        data["query"] = query
        response = requests.post(url=url, params=data)
        response.raise_for_status()
        print(response.text)

def start_server():
    port = PORT

    key = ""
    uuid_str = str(uuid.uuid4())
    with open(os.path.join(APP_PATH, "key.txt"), 'r') as f:
        keys = f.readlines()
        if len(keys) > 0:
            key = keys[0].strip()
    
    print(f"start with key {key}")
    application = tornado.web.Application(
        [
            (r"/", MainHandler, dict(key=key, uuid=uuid_str)),
            (r"/erge", ErgeHandler, dict(key=key, uuid=uuid_str)), # 儿歌
            (r"/chengyu", ChengyuHandler, dict(key=key, uuid=uuid_str)), # 成语故事
            (r"/ip_check", IPCheckHandler, dict(key=key, uuid=uuid_str)), # 本地IP
            (r"/weather", WeatherHandler, dict(key=key, uuid=uuid_str)), # 天气预报
            (
                r"/photo/(.+\.(?:png|jpg|jpeg|bmp|gif|JPG|PNG|JPEG|BMP|GIF))",
                tornado.web.StaticFileHandler,
                {"path": "static"},
            ),
            (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "static"}),
        ],
        **settings,
    )

    try:
        asyncio.set_event_loop(asyncio.new_event_loop())
        application.listen(int(port))
        tornado.ioloop.IOLoop.instance().start()
    except Exception as e:
        logger.critical(f"服务器启动失败: {e}", stack_info=True)


def run(debug=False):
    settings["debug"] = debug
    t = threading.Thread(target=lambda: start_server())
    t.start()

run(True)