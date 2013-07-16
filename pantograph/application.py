import tornado.web
import tornado.ioloop
import json
import os
from .handlers import *
from . import static

class PantographApplication(tornado.web.Application):
    def __init__(self, websock_handlers, **settings):
        constr_args = dict(settings)
        
        if os.path.isfile("./config.json"):
            f = open("./config.json")
            constr_args.update(json.load(f))

        constr_args["static_path"] = os.path.dirname(static.__file__)

        handlers = []

        for title, url, handler in websock_handlers:
            handlers.append((url, MainCanvasHandler, 
                            {"title" : title, "url" : url}))
            handlers.append((os.path.join(url, "socket"), handler))

        tornado.web.Application.__init__(self, handlers, **constr_args)

    def run(self, address = "127.0.0.1", port = 8080):
        self.listen(port, address)
        print("Pantograph now running at http://" + address + ":" + str(port))
        tornado.ioloop.IOLoop.instance().start()
