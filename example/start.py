import sys
sys.path.append('..')

import pantograph
import tornado.web

handlers = [
    (r"/", pantograph.MainCanvasHandler, {"title" : "Pantograph Example"})
]

if __name__ == '__main__':
    app = pantograph.PantographApplication(handlers)
    app.run()
