# Pantograph: HTML5 Canvas Drawing in Python

Pantograph is a library for writing HTML5 canvas animations and games in Python.
It is meant to provide a simple and easy-to-use Python interface to the canvas 
for beginning programmers who have not yet learned Javascript.

Pantograph uses the Tornado networking library to send drawing commands and
receive input events from the browser through websockets. Thus, Tornado is
the only dependency.

## Example Program

```python
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
```

This program is located at "examples/rotary/start.py".

## API

### PantographApplication

This class is the main application, which can hold one or more handlers.
The required constructor argument is a list of 3-tuples containing the name
of the handler, the url, and the handler class. For instance,

```python
pantograph.PantographApplication([
	("Pantograph", "/", pantograph.PantographHandler)
])
```

It has one public method `run` which starts the application server. 
By default, the server runs on port 8080 and is bound to localhost.
You can, however, override these defaults by providing extra arguments.
For instance, if you replaced `app.run()` with `app.run("0.0.0.0", 8000)`,
the server would be publically accessible on port 8000.

### SimplePantographApplication

A subclass of `PantographApplication` which takes in a single handler and
sets up a route to it from the root url. The name is take from the class name
of the handler.

### PantographHandler

This class contains event handlers for various mouse and keyboard events, 
a continuous timer, and methods for drawing on the canvas. 
Create a subclass of `PantographHandler` to implement your application.

#### Main Hooks

`setup()` - Called once when the handler is initialized. Override this method
to put in any one-off setup code.

`update()` - Called in the main loop of the application. Override this method to
put in any update code, such as redrawing a frame.

#### Drawing Methods

`draw_rect(x, y, width, height, color = "#000")` - Draw a hollow rectangle
on the canvas. The color argument is the line color and takes any valid CSS 
color definition as a string. The other arguments are self-explanatory.

`fill_rect(x, y, width, height, color = "#000")` - Draw a filled rectangle on
the canvas. The color argument here is the fill color.

`clear_rect(x, y, width, height)` - Clear a rectangular area of the canvas.

`draw_oval(x, y, width, height, color = "#000")` - Draw a hollow oval on the
canvas.

`fill_oval(x, y, width, height, color = "#000")` - Draw a filled oval on the
canvas.

`draw_circle(x, y, radius, color = "#000")` - Draw a hollow circle on the 
canvas. The x and y are the x and y or the center of the circle.

`fill_circle(x, y, radius, color = "#000")` - Draw a filled circle on the 
canvas. 
    
`draw_line(self, startX, startY, endX, endY, color = "#000")` - Draw a line
from (startX, startY) to (endX, endY).

`draw_polygon(self, points, color = "#000")` - Draw a hollow polygon on the
canvas. The `points` argument is a list of (x, y) pairs.

`fill_polygon(self, points, color = "#000")` - Draw a filled polygon on the
canvas.

`draw_image(self, name, x, y, width=None, height=None)` - Draw an image on
the canvas. The `name` parameter is the name of the image, pantograph will
search for an image by that name in your current directory at
"images/*handler_name*/*name*" and then at "images/*name*" where *handler_name*
is the name of your handler, and *name* is the name passed the function.
If you do not supply a width or a height, the actual width and height of the
image will be used.

#### Event Callbacks

All event callbacks are passed an `InputEvent` object which contains the
following fields.

 * `x` - The x position of the mouse
 * `y` - The y position of the mouse
 * `button` - Which button on the mouse was pressed (0 - left, 1 - middle, 2 - right)?
 * `alt_key` - Was the alt key held down?
 * `ctrl_key` - Was the ctrl key held down?
 * `meta_key` - Was the meta (Windows) key held down?
 * `shift_key` - Was the shift key held down?
 * `key_code` - The key code

The following are the callback methods which can be overloaded. 
The callbacks correspond directly to HTML DOM events.

 * `on_mouse_down` - Called when a mouse button is pressed down
 * `on_mouse_up` - Called when a mouse button is released
 * `on_mouse_move` - Called when the mouse is moved across the canvas
 * `on_click` - Called when the mouse is clicked (pressed and released)
 * `on_dbl_click` - Called when the mouse is double-clicked
 * `on_key_down` - Called when a keyboard key is pushed down
 * `on_key_up` - Called when a key is released
 * `on_key_press` - Called periodically while key is held down

#### Instance variables

 * `width` - The width of the canvas
 * `height` - The height of the canvas

### Shape Objects

Pantograph also provides a set of shape classes to represent your animation
in an object oriented manner. The shape objects correspond to the `draw_*` 
methods in the handler class.

 * `Rect(x, y, width, height, fill_color=None, line_color=None)` - 
 	If no values are provided for `fill_color` or `line_color`, 
	the fill or line will be transparent
 * `Oval(x, y, width, height, fill_color=None, line_color=None)`
 * `Circle(x, y, radius, fill_color=None, line_color=None)`
 * `Image(img_name, x, y, width=None, height=None)`
 * `Line(startx, starty, endx, endy, color = None)`
 * `Polygon(points, fill_color=None, line_color=None)`
 * `CompoundShape(shapes)` - `shapes` is a list of other shape objects

#### Shape Methods

 * `draw(canvas)` - Draw the shape on the `canvas`, which is an instance of
   `PantographHandler`.
 * `translate(dx, dy)` - Move the shape across the screen
 * `rotate(theta)` - Rotate the shape to the angle `theta`, which is in 
    radians. The angle `theta = 0` would be facing directly to the right,
	and increases in the clockwise direction.
 * `intersects(other)` - Determine if this shape intersects with the `other` shape
 * `contains(other)` - Determine if this shape wholly encompasses the `other` shape

## Configuration

You can configure your application by putting a "config.json" file in your
current directory. The json file should contain a dictionary which can have
any of the following keys.

 * `timer_interval` - The number of milliseconds between each call to the
 `update` method.
 * `width` - The width of the canvas on the screen. This can be an integer or
 the string "fullWidth" to fill up the entire width of the browser.
 * `height` - The height of the canvas on the screen. This can be an integer
 or the string "fullHeight" to fill up the entire height of the browser.

If you have multiple handlers in your application, you can configure each 
handler separately by associating a key with the handler's name to a nested 
dictionary containing any of the variables above.
