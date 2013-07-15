import tornado.web
import tornado.template

import templates

class MainCanvasHandler(tornado.web.RequestHandler):
    def initialize(self, title = "Pantograph"):
        self.title = title

    def get(self):
        t = tornado.template.Template(templates.MAIN_CANVAS)
        self.write(t.generate(title = self.title))
