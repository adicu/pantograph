import sys
sys.path.append('..')

import pantograph
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, World!")

handlers = [
    (r"/", MainHandler)
]

if __name__ == '__main__':
    app = pantograph.PantographApplication(handlers)
    app.run()
