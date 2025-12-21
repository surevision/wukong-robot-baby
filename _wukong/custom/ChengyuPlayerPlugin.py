# -*- coding: utf-8 -*-
import os
import re
import random
import platform

from robot import config, logging
from robot.Player import MusicPlayer
from robot.sdk.AbstractPlugin import AbstractPlugin

logger = logging.getLogger(__name__)


class Plugin(AbstractPlugin):

    SLUG = "ChengYuGuShi"

    IS_IMMERSIVE = True  # 这是个沉浸式技能

    def __init__(self, con):
        super(Plugin, self).__init__(con)
        self.player = None
        self.song_list = None
        self.song_titles = None

    def get_song_list(self, path):
        song_list = []
        song_titles = []
        if not os.path.exists(path):
            return [], []
        with open(path, 'r') as f:
            for line in f.readlines():
                song_title = line.split("$")[0]
                song_path = line.split("$")[1]
                song_titles.append(song_title)
                song_list.append(song_path)
        return song_titles, song_list

    def init_music_player(self):
        self.song_titles, self.song_list = self.get_song_list(config.get("/ChengyuPlayer/path"))
        if self.song_list == None:
            logger.error(f"{self.SLUG} 插件配置有误", stack_info=True)
        logger.info(f"成语故事列表：{self.song_list}")
        return MusicPlayer(self.song_list, self)

    def handle(self, text, parsed):
        
        patterns = [re.compile("(.*?)随便(.*?)成语故事(.*?)"),
                re.compile("(.*?)播放(.*?)成语故事(.*?)"),
                re.compile("(.*?)随机(.*?)成语故事(.*?)"),
                re.compile("(.*?)讲一个成语故事(.*?)"),
                re.compile("(.*?)讲个成语故事(.*?)")]

        pattern_cert_1 = re.compile("(.*?)讲成语故事(.+)")
        
        pattern_cert_ctr_1 = re.compile("(.*?)下一个成语故事(.*?)")
        pattern_cert_ctr_2 = re.compile("(.*?)上一个成语故事(.*?)")
        pattern_cert_ctr_3 = re.compile("(.*?)停止成语故事(.*?)")

        if not self.player:
            self.player = self.init_music_player()
        if len(self.song_list) == 0:
            self.clearImmersive()  # 去掉沉浸式
            self.say("未指定成语故事文件，播放失败")
            return

        if any(re.match(pattern, text) is not None for pattern in patterns):
            logger.info("开始随机播放")
            self.player.play(random.randrange(len(self.song_list)))
        elif (re.match(pattern_cert_1, text) is not None):
            idx = -1
            i = 0
            m = re.search(pattern_cert_1, text)
            logger.info(f"查找成语故事：{m.group(1)}")
            for song in self.song_titles:
                if song in m.group(2):
                    idx = i
                    break
                i += 1
            if idx >= 0:
                logger.info("开始播放指定的成语故事")
                self.player.play(idx)
            else:
                self.say("没有找到这个成语故事")
        elif (re.match(pattern_cert_ctr_1, text) is not None):
            self.player.next()
        elif (re.match(pattern_cert_ctr_2, text) is not None):
            self.player.prev()
        elif (re.match(pattern_cert_ctr_3, text) is not None):
            logger.info("停止播放")
            self.player.stop()
            self.clearImmersive()  # 去掉沉浸式
        else:
            self.say("没听懂你的意思呢，要停止播放，请说停止播放")
            self.player.resume()

    def pause(self):
        if self.player:
            system = platform.system()
            # BigSur 以上 Mac 系统的 pkill 无法正常暂停音频，
            # 因此改成直接停止播放，不再支持沉浸模式
            if system == "Darwin" and float(platform.mac_ver()[0][:5]) >= 10.16:
                logger.warning("注意：Mac BigSur 以上系统无法正常暂停音频，将停止播放，不支持恢复播放")
                self.player.stop()
                return
            self.player.pause()

    def restore(self):
        if self.player and self.player.is_pausing():
            self.player.resume()

    def isValidImmersive(self, text, parsed):
                
        pattern_cert_ctr_1 = re.compile("(.*?)下一个成语故事(.*?)")
        pattern_cert_ctr_2 = re.compile("(.*?)上一个成语故事(.*?)")
        pattern_cert_ctr_3 = re.compile("(.*?)停止成语故事(.*?)")

        return re.match(pattern_cert_ctr_1, text) or re.match(pattern_cert_ctr_2, text) or re.match(pattern_cert_ctr_3, text)

    def isValid(self, text, parsed):
        patterns = [re.compile("(.*?)随便(.*?)成语故事(.*?)"),
                re.compile("(.*?)播放(.*?)成语故事(.*?)"),
                re.compile("(.*?)随机(.*?)成语故事(.*?)"),
                re.compile("(.*?)讲一个成语故事(.*?)"),
                re.compile("(.*?)讲个成语故事(.*?)")]

        pattern_cert_1 = re.compile("(.*?)讲成语故事(.+)")

        return any(re.match(pattern, text) is not None for pattern in patterns) or re.match(pattern_cert_1, text)
