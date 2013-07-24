from collections import namedtuple

BoundingRect = namedtuple('BoundingRect', ['left', 'top', 'right', 'bottom'])
Point = namedtuple('Point', ['x', 'y'])

class Shape(object):
    def get_bounding_rect(self):
        raise NotImplementedError

    def draw(self, canvas):
        canvas.draw(self.shape_type(), **self.to_dict())

    def translate(self, dx, dy):
        raise NotImplementedError

    def to_dict(self):
        raise NotImplementedError

    def rotate(self, theta):
        if theta == 0:
            self.rotation = None
        else:
            rect = self.get_bounding_rect()
            rotx = (rect.left + rect.right) / 2
            roty = (rect.top + rect.bottom) / 2
            self.rotation = dict(x=rotx, y=roty, theta=theta)

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

    def shape_type(self):
        return type(self).__name__.lower()


class SimpleShape(Shape):
    def __init__(self, x, y, width, height, fill_color=None, line_color=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fill_color = fill_color
        self.line_color = line_color
        self.rotation = None
    
    def get_bounding_rect(self):
        return BoundingRect(self.x, self.y, 
                            self.x + self.width, 
                            self.y + self.height)
    
    def translate(self, dx, dy):
        self.x += dx
        self.y += dy

    def to_dict(self):
        return dict(x = self.x, y = self.y,
                    width = self.width, height = self.height,
                    fillColor = self.fill_color, lineColor = self.line_color,
                    rotate = self.rotation)
        
class Rect(SimpleShape):
    pass
    
class Oval(SimpleShape):
    pass

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

    def to_dict(self):
        return dict(x = self.x, y = self.y, radius = self.radius,
                    fillColor = self.fill_color, lineColor = self.line_color)

class Image(SimpleShape):
    def __init__(self, img_name, x, y, width=None, height=None):
        self.img_name = img_name
        super(Image, self).__init__(x, y, width, height)

    def draw(self, canvas):
        canvas.draw_image(self.img_name, self.x, self.y, 
                          self.width, self.height,
                          rotate = self.rotation)

class Line(Shape):
    def __init__(self, startx, starty, endx, endy, color = None):
        self.startx = startx
        self.starty = starty
        self.endx = endx
        self.endy = endy
        self.color = color

    def to_dict(self):
        return dict(startX = self.startx, startY = self.starty,
                    endX = self.endx, endY = self.endy, 
                    color = self.color, rotate = self.rotation)

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
        
        self.minx = min(pt[0] for pt in points)
        self.maxx = max(pt[0] for pt in points)
        self.miny = min(pt[1] for pt in points)
        self.maxy = max(pt[1] for pt in points)

    def translate(self, dx, dy):
        self.minx += dx
        self.maxx += dx
        self.miny += dy
        self.maxy += dy

        self.points = [Point(p.x + dx, p.y + dy) for p in self.points]

    def to_dict(self):
        return dict(points = self.points, 
                    fillColor = self.fill_color,
                    lineColor = self.line_color,
                    rotate = self.rotation)

    def get_bounding_rect(self):
        return BoundingRect(self.minx, self.miny, self.maxx, self.maxy)

class CompoundShape(Shape):
    def __init__(self, shapes):
        self.shapes = shapes
        rects = [shp.get_bounding_rect() for shp in shapes]
        
        self.left = min(rct.left for rct in rects)
        self.right = max(rct.right for rct in rects)
        self.top = min(rct.top for rct in rects)
        self.bottom = max(rct.bottom for rct in rects)

    def translate(self, dx, dy):
        for shp in self.shapes:
            shp.translate(dx, dy)
        self.left += dx
        self.right += dx
        self.top += dy
        self.bottom += dy

    def get_bounding_rect(self):
        return BoundingRect(self.left, self.top, self.right, self.bottom)

    def to_dict(self):
        return dict(shapes=[dict(shp.to_dict(), type=shp.shape_type()) 
                            for shp in self.shapes],
                    rotate = self.rotation)

    def shape_type(self):
        return "compound"
