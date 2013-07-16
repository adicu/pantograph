import sys
import pantograph

class MyPantoHandler(pantograph.PantographHandler):
    def on_mouse_press(self, event):
        print("Mouse pressed")

if __name__ == '__main__':
    app = pantograph.PantographApplication([
        ("Pantograph", "/", MyPantoHandler)
    ])
    app.run()
