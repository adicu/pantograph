import tornado.web
import tornado.ioloop
import json
import os
from .handlers import *

CONSTRUCTOR_SETTINGS = ["debug", "gzip", "cookie_secret", "login_url",
                        "xsrf_cookies", "autoescape", "template_path", 
                        "static_path", "static_url_prefix"]

class PantographApplication(tornado.web.Application):
    def __init__(self, websock_handler, websock_handler_args = {}, 
                 appname = "Pantograph", prefix = "/", **settings):
        self.settings = settings
        if os.path.isfile("./config.json"):
            f = open("./config.json")
            self.settings.update(json.load(f))

        constr_args = {}
        for key in CONSTRUCTOR_SETTINGS:
            if key in self.settings:
                constr_args[key] = self.settings[key]

        handlers = [
            (prefix, MainCanvasHandler, {"title": appname}),
            (prefix + "socket", websock_handler, websock_handler_args)
        ]

        tornado.web.Application.__init__(self, handlers, **constr_args)

    def run(self, address = "127.0.0.1", port = 8080):
        self.listen(port, address)
        print("Pantograph now running at http://" + address + ":" + str(port))
        tornado.ioloop.IOLoop.instance().start()
