import tornado.web
import tornado.websocket
import tornado.template
from tornado.ioloop import IOLoop

import random
import json
import os
import datetime

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
        event_type = message.get("event_type")
        event_callbacks = {
            "mouse_press": self.on_mouse_press,
            "mouse_release": self.on_mouse_release,
            "mouse_move": self.on_mouse_move,
            "mouse_drag": self.on_mouse_drag,
            "key_press": self.on_key_press,
            "key_release": self.on_key_release,
        }
        event_callbacks[event_type](message.get("event"))

    def timeout(self):
        self.update()
        delta = datetime.timedelta(milliseconds = self.interval)
        IOLoop.current().add_timeout(delta, self.timeout)

    def update(self):
        pass

    def on_mouse_press(self, event):
        pass

    def on_mouse_release(event):
        pass

    def on_key_press(self, event):
        pass

    def on_key_release(self, event):
        pass

    def on_mouse_move(self, event):
        pass

    def on_mouse_drag(self, event):
        pass
