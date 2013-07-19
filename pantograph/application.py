import tornado.web
import tornado.ioloop
import json
import os
from .handlers import *
from . import js

class PantographApplication(tornado.web.Application):
    def __init__(self, websock_handlers, **settings):
        constr_args = dict(settings)
        
        if os.path.isfile("./config.json"):
            f = open("./config.json")
            constr_args.update(json.load(f))

        js_path = os.path.dirname(js.__file__)

        handlers = [
            (r"/js/(.*\.js)", tornado.web.StaticFileHandler, {"path":  js_path}),
            (r"/img/(.*)", tornado.web.StaticFileHandler, {"path": "./images"})
        ]

        for name, url, ws_handler in websock_handlers:
            handlers.append((url, MainPageHandler, 
                            {"name" : name, "url" : url}))
            handlers.append((os.path.join(url, "socket"), ws_handler,
                            {"name": name}))

        tornado.web.Application.__init__(self, handlers, **constr_args)

    def run(self, address = "127.0.0.1", port = 8080):
        self.listen(port, address)
        print("Pantograph now running at http://" + address + ":" + str(port))
        tornado.ioloop.IOLoop.instance().start()

class SimplePantographApplication(PantographApplication):
    def __init__(self, handler, **settings):
        PantographApplication.__init__(
            self, [(handler.__name__, "/", handler)], **settings)
