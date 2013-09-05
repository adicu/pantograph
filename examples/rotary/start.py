import pantograph
import math

# Animate a spinning wheel on the canvas 

class Rotary(pantograph.PantographHandler):
    def setup(self):
        self.angle = 0
        self.radius = min(self.width, self.height) / 2
    
    def update(self):
        cx = self.radius
        cy = self.radius

        self.clear_rect(0, 0, self.width, self.height)
        # draw the circle for the "rim" of the wheel
        self.draw_circle(self.radius, self.radius, self.radius, "#f00")
        
        # draw eight evenly-spaced "spokes" from the center to the edge
        for i in range(0, 8):
            angle = self.angle + i * math.pi / 4
            x = cx + self.radius * math.cos(angle)
            y = cy + self.radius * math.sin(angle)
            self.draw_line(cx, cy, x, y, "#f00")

        self.angle += math.pi / 64
    
if __name__ == '__main__':
    app = pantograph.SimplePantographApplication(Rotary)
    app.run()
