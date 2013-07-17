import tornado.web
import tornado.websocket
import tornado.template
from tornado.ioloop import IOLoop

import random
import json
import os
import datetime
from collections import namedtuple

from . import templates

LOADER = tornado.template.Loader(os.path.dirname(templates.__file__))

class MainPageHandler(tornado.web.RequestHandler):
    def initialize(self, title, url):
        self.title = title
        self.url = url
    def get(self):
        t = LOADER.load("index.html")
        
        width = self.settings.get("canvasWidth", "fullWidth")
        height = self.settings.get("canvasHeight", "fullHeight")
        
        if self.title in self.settings:
            width = self.settings[self.title].get("canvasWidth", width)
            height = self.settings[self.title].get("canvasHeight", height)

        ws_url = os.path.join(self.url, "socket")
        
        self.write(t.generate(
            title = self.title, url = self.url, ws_url = ws_url,
            width = width, height = height))

DEFAULT_INTERVAL = 100

InputEvent = namedtuple("InputEvent", ["type", "x", "y", "button", 
                                       "alt_key", "ctrl_key", "meta_key",
                                       "shift_key", "key_code"])

class PantographHandler(tornado.websocket.WebSocketHandler):
    def initialize(self, name):
        self.name = name
        interval = self.settings.get("timer_interval", DEFAULT_INTERVAL)
        if self.name in self.settings:
            interval = self.settings[self.name].get("timer_interval", interval)
        self.interval = interval

    def open(self):
        # randomize the first timeout so we don't get every timer
        # expiring at the same time
        interval = random.randint(1, self.interval)
        delta = datetime.timedelta(milliseconds = interval)
        IOLoop.current().add_timeout(delta, self.timeout)

    def on_message(self, raw_message):
        message = json.loads(raw_message)
        event_type = message.get("type")
        event_callbacks = {
            "mousedown": self.on_mouse_down,
            "mouseup": self.on_mouse_up,
            "mousemove": self.on_mouse_move,
            "click": self.on_click,
            "dblclick": self.on_dbl_click,
            "keydown": self.on_key_down,
            "keyup": self.on_key_up,
            "keypress": self.on_key_press
        }
        event_callbacks[event_type](InputEvent(**message))

    def timeout(self):
        self.update()
        delta = datetime.timedelta(milliseconds = self.interval)
        IOLoop.current().add_timeout(delta, self.timeout)

    def update(self):
        pass

    def on_mouse_down(self, event):
        pass

    def on_mouse_up(self, event):
        pass
    
    def on_mouse_move(self, event):
        pass

    def on_click(self, event):
        pass

    def on_dbl_click(self, event):
        pass

    def on_key_down(self, event):
        pass

    def on_key_up(self, event):
        pass

    def on_key_press(self, event):
        pass
