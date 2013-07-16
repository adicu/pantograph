import sys
sys.path.append('..')

import pantograph
import tornado.web
import tornado.websocket

class MyPantoHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        pass

    def on_message(self, message):
        print(message)

    def on_close(self):
        pass

if __name__ == '__main__':
    app = pantograph.PantographApplication(MyPantoHandler)
    app.run()
