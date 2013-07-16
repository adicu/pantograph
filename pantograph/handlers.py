import tornado.web
import tornado.template

from . import templates
import os

LOADER = tornado.template.Loader(os.path.dirname(templates.__file__))

class MainCanvasHandler(tornado.web.RequestHandler):
    def initialize(self, title = "Pantograph"):
        self.title = title

    def get(self):
        t = LOADER.load("index.html")
        self.write(t.generate(title = self.title))
