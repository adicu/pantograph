from collections import namedtuple

BoundingRect = namedtuple('BoundingRect', ['left', 'top', 'right', 'bottom'])
Point = namedtuple('Point', ['x', 'y'])

class Shape(object):
    def get_bounding_rect(self):
        raise NotImplementedError

    def draw(self, canvas):
        raise NotImplementedError

    def translate(self, dx, dy):
        raise NotImplementedError

    def intersects(self, other):
        recta = self.get_bounding_rect()
        rectb = other.get_bounding_rect()
        
        if (recta.left < rectb.left):
            cleft = rectb.left
            cright = recta.right
        elif (recta.left > rectb.left):
            cleft = recta.left
            cright = rectb.right
        elif (recta.right < rectb.right):
            cleft = recta.left
            cright = recta.right
        else:
            cleft = rectb.left
            cright = rectb.right

        if (recta.top < rectb.top):
            ctop = rectb.top
            cbottom = recta.bottom
        elif (recta.top > rectb.top):
            ctop = recta.top
            cbottom = rectb.bottom
        elif (recta.bottom < rectb.bottom):
            ctop = recta.top
            cbottom = recta.bottom
        else:
            ctop = rectb.top
            cbottom = rectb.bottom

        return cleft < cright and ctop < cbottom

    def contains(self, other):
        if isinstance(other, Point):
            rect = self.get_bounding_rect()
            return rect.left < x and rect.right > x and \
                    rect.top < y and rect.bottom > y

        recta = self.get_bounding_rect()

        if isinstance(other, Shape):
            rectb = other.get_bounding_rect()
        elif isinstance(other, BoundingRect):
            rectb = other
        else:
            raise ValueError("other must be a Shape, BoundingRect, or Point")

        return recta.left < rectb.left and recta.right > rectb.right and \
                recta.top < rectb.top and recta.bottom > rectb.bottom

class SimpleShape(Shape):
    def __init__(self, x, y, width, height, fill_color=None, line_color=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fill_color = fill_color
        self.line_color = line_color

    
    def get_bounding_rect(self):
        return BoundingRect(self.x, self.y, 
                            self.x + self.width, 
                            self.y + self.height)
    
    def translate(self, dx, dy):
        self.x += dx
        self.y += dy

class Rect(SimpleShape):
    def draw(self, canvas):
        if self.fill_color is not None:
            canvas.fill_rect(self.x, self.y, 
                             self.width, self.height, 
                             self.fill_color)
        if self.line_color is not None:
            canvas.draw_rect(self.x, self.y, 
                             self.width, self.height, 
                             self.line_color)
    
class Oval(SimpleShape):
    def draw(self, canvas):
        if self.fill_color is not None:
            canvas.fill_oval(self.x, self.y, 
                             self.width, self.height, 
                             self.fill_color)
        if self.line_color is not None:
            canvas.draw_oval(self.x, self.y, 
                             self.width, self.height, 
                             self.line_color)

class Circle(SimpleShape):
    def __init__(self, x, y, radius, fill_color=None, line_color=None):
        self.x = x
        self.y = y
        self.radius = radius
        self.fill_color = fill_color
        self.line_color = line_color
    
    def get_bounding_rect(self):
        return BoundingRect(self.x - self.radius, self.y - self.radius,
                            self.x + self.radius, self.y + self.radius)

    def draw(self, canvas):
        if self.fill_color is not None:
            canvas.fill_circle(self.x, self.y, self.radius, self.fill_color)
        if self.line_color is not None:
            canvas.draw_oval(self.x, self.y, self.radius, self.line_color)

class Image(SimpleShape):
    def __init__(self, img_name, x, y, width=None, height=None):
        self.img_name = img_name
        super(Image, self).__init__(x, y, width, height)

    def draw(self, canvas):
        canvas.draw_image(self.img_name, self.x, self.y, 
                          self.width, self.height)

class Line(Shape):
    def __init__(self, startx, starty, endx, endy, color = None):
        self.startx = startx
        self.starty = starty
        self.endx = endx
        self.endy = endy
        self.color = color

    def draw(self, canvas):
        if color is not None:
            canvas.draw_line(self.startx, self.starty, self.endx, seld.endy)

    def get_bounding_rect(self):
        if self.startx < self.endx:
            left = self.startx
            right = self.endx
        else:
            left = self.endx
            right = self.startx

        if self.starty < self.endy:
            top = self.starty
            bottom = self.endy
        else:
            top = self.endy
            bottom = self.starty

        return BoundingRect(left, top, right, bottom)

    def translate(self, dx, dy):
        self.startx += dx
        self.starty += dy
        self.endx += dx
        self.endy += dy

class Polygon(Shape):
    def __init__(self, points, fill_color=None, line_color=None):
        self.points = [Point(x, y) for (x, y) in points]
        self.line_color = line_color
        self.fill_color = fill_color
        
        self.minx = points[0][0]
        self.maxx = points[0][0]
        self.miny = points[0][1]
        self.maxy = points[0][1]

        for (x, y) in points[1:]:
            if x < self.minx:
                self.minx = x
            if x > self.maxx:
                self.maxx = x
            
            if y < self.miny:
                self.miny = y
            if x > self.maxy:
                self.maxy = y

    def translate(self, dx, dy):
        self.minx += dx
        self.maxx += dx
        self.miny += dy
        self.maxy += dy

        self.points = [Point(p.x + dx, p.y + dy) for p in self.points]

    def draw(self, canvas):
        if self.line_color is not None:
            canvas.draw_polygon(self.points, self.line_color)
        elif self.fill_color is not None:
            canvas.fill_polygon(self.points, self.fill_color)

    def get_bounding_rect(self):
        return BoundingRect(self.minx, self.miny, self.maxx, self.maxy)
