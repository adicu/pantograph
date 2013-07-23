import sys
import pantograph
import random

class BouncingShape(object):
    def __init__(self, shape, xvel, yvel):
        self.shape = shape
        self.xvel = xvel
        self.yvel = yvel

    def update(self, canvas):
        rect = self.shape.get_bounding_rect()

        if rect.left <= 0 or rect.right >= canvas.width:
            self.xvel *= -1
        if rect.top <= 0 or rect.bottom >= canvas.height:
            self.yvel *= -1

        self.shape.translate(self.xvel, self.yvel)
        self.shape.draw(canvas)

class BouncingBallDemo(pantograph.PantographHandler):
    def setup(self):
        self.xvel = random.randint(1, 5)
        self.yvel = random.randint(1, 5)

        static_shapes = [
            pantograph.Image("baseball.jpg", 100, 100, 20, 20),
            pantograph.Rect(120, 150, 20, 20, "#f00"),
            pantograph.Circle(15, 300, 10, "#0f0"),
            pantograph.Polygon([
                (10, 10),
                (5, 20),
                (30, 30)
            ], "#00f")
        ]

        self.shapes = [BouncingShape(shp, random.randint(1, 5),
                                          random.randint(1, 5))
                        for shp in static_shapes]

    def update(self):
        self.clear_rect(0, 0, self.width, self.height)

        for shape in self.shapes:
            shape.update(self)


if __name__ == '__main__':
    app = pantograph.SimplePantographApplication(BouncingBallDemo)
    app.run()
