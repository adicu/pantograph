import sys
import pantograph
import random
import math
import itertools

class BouncingShape(object):
    def __init__(self, shape):
        self.shape = shape
        self.theta = 0
        self.xvel = random.randint(1, 5)
        self.yvel = random.randint(1, 5)
        self.rvel = (math.pi / 2) * random.random()

    def update(self, canvas):
        rect = self.shape.get_bounding_rect()

        if rect.left <= 0 or rect.right >= canvas.width:
            self.xvel *= -1
        if rect.top <= 0 or rect.bottom >= canvas.height:
            self.yvel *= -1

        self.theta += self.rvel
        if self.theta > math.pi:
            self.theta -= 2 * math.pi

        self.shape.translate(self.xvel, self.yvel)
        self.shape.rotate(self.theta)
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
                (60, 10),
                (55, 20),
                (80, 30)
            ], "#00f"),
            pantograph.CompoundShape([
                pantograph.Rect(15, 15, 10, 10, "#0ff"),
                pantograph.Circle(20, 20, 5, "#ff0")
            ])
        ]

        self.shapes = [BouncingShape(shp) for shp in static_shapes]

    def update(self):
        self.clear_rect(0, 0, self.width, self.height)

        for shape in self.shapes:
            shape.update(self)

        for (a, b) in itertools.combinations(self.shapes, 2):
            if a.shape.intersects(b.shape):
                xveltmp = a.xvel
                yveltmp = a.yvel
                a.xvel = b.xvel
                a.yvel = b.yvel
                b.xvel = xveltmp
                b.yvel = yveltmp

if __name__ == '__main__':
    app = pantograph.SimplePantographApplication(BouncingBallDemo)
    app.run()
