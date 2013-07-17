import sys
import pantograph

class MyPantoHandler(pantograph.PantographHandler):
    def on_click(self, event):
        mess = "Button %d clicked at %d, %d" % (event.button, event.x, event.y)
        print(mess)

if __name__ == '__main__':
    app = pantograph.PantographApplication([
        ("Pantograph", "/", MyPantoHandler)
    ])
    app.run()
