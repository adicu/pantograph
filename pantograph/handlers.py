import tornado.web
import tornado.template

from . import templates
import os

LOADER = tornado.template.Loader(os.path.dirname(templates.__file__))

class MainCanvasHandler(tornado.web.RequestHandler):
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
        
        self.write(t.generate(
            title = self.title, url = self.url,
            width = width, height = height))
