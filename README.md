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
import random

class BouncingBallHandler(pantograph.PantographHandler):
    def setup(self):
        self.x = 100
        self.y = 100
        self.xvel = random.randint(1, 5)
        self.yvel = random.randint(1, 5)

    def update(self):
        if self.x <= 0 or self.x >= self.width:
            self.xvel *= -1
        if self.y <= 0 or self.y >= self.height:
            self.yvel *= -1

        self.x += self.xvel
        self.y += self.yvel

        self.clear_rect(0, 0, self.width, self.height)
        self.fill_circle(self.x, self.y, 10, "#f00")

if __name__ == '__main__':
    app = pantograph.SimplePantographApplication(BouncingBall)
    app.run()
```

## API

### PantographApplication

This class is the main application, which can hold one or more handlers.
The required constructor argument is a list of 3-tuples containing the name
of the handler, the url, and the handler class.

It has one public method `run` which starts the application server. 
By default, the server runs on port 8080 and is bound to localhost.
You can, however, override these defaults by providing extra arguments.
For instance, if you replaced `app.run()` with `app.run("0.0.0.0", 8000)`,
the server would be publically accessible on port 8000.

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
