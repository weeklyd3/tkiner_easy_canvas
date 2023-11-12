this basically imitates p5.js in canvas

usage:
```py
# initialize window in Tkinter
from tkinter import Tk
window = Tk()
# create canvas
from tkinter_easy_canvas import EasyCanvas
draw = EasyCanvas(640, 480, window)
# add canvas to window
draw.grid()
draw.fill('red')
draw.rect(0, 0, 100, 100)
# display window
window.mainloop()
```