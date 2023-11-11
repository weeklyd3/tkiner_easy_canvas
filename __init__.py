from tkinter import *
from threading import Thread
from time import time_ns, sleep
DEFAULT_CONFIG = {
	'fill': 'black',
	'stroke': '',
	'translate': [0, 0],
	'textFont': 'default',
	'textSize': 12
}
class Config:
	def __init__(self, parent, config = {}):
		self.config = config
		self.parent = parent
		self.pushed_states = []
	def push(self):
		self.pushed_states.append(self.config)
		for key in self.config.keys(): self.config[key] = DEAULT_CONFIG[key]
	def pop(self):
		if not len(self.pushed_states): return
		to_restore = self.pushed_states.pop()
		for key in to_restore.keys(): self.config[key] = to_restore[key]
	def get(self, key, default = None):
		if key in self.config.keys(): return self.config[key]
		else: return default
	def set(self, key, value): self.config[key] = value
class EasyCanvas(Canvas):
	def __init__(self, width, height, parent = None):
		super().__init__(parent, width = width, height = height)
		self._config = Config(self, DEFAULT_CONFIG)
	def _coordinates(self, coords):
		'''
		Translates coordinates. coords[0] += translate[0],
		and coords[1] += translate[1], where translate is
		the sum of translated positions or [0, 0].
		'''
		translate=  self._config.get('translate')
		coords[0] += translate[0]
		coords[1] += translate[1]
		return coords
	def clear(self): self.delete('all')

	# configuration wrappers
	def fill(self, color): self._config.set('fill', color)
	def stroke(self, color): self._config.set('outline', color)
	def translate(self, x, y): 
		translate = self._config.get('translate')
		new_translate = [translate[0] + x, translate[1] + y]
		self._config.set('translate', new_translate)
	def reset_translate(self): self._config.set('translate', [0, 0])
	def textFont(self, font): self._config.set('textFont', font)
	def textSize(self, size): self._config.set('textSize', size)
	def push(self): self._config.push()
	def pop(self): self._config.pop()

	# wrappers around canvas.create_* functions
	def rect(self, x, y, width, height):
		self.create_rectangle(
			*self._coordinates([x, y]),
			*self._coordinates([x + width, y + height]),
			fill = self._config.get('fill'),
			outline = self._config.get('stroke')
		)
	def circle(self, x, y, diameter):
		radius = diameter / 2
		self.create_oval(
			*self._coordinates([x - radius, y - radius]),
			*self._coordinates([x + radius, y + radius]),
			fill = self._config.get('fill'),
			outline = self._config.get('stroke')
		)
	def line(self, x1, y1, x2, y2):
		self.create_line(
			*self._coordinates([x1, y1]),
			*self._coordinates([x2, y2]),
			fill = self._config.get('fill')
		)
	def text(self, text, x1, y1):
		self.create_text(
			x1,
			y1,
			text = text,
			fill = self._config.get('fill'),
			font = (
				self._config.get('textFont'),
				self._config.get('textSize')
			)
		)
	# animation
	def animate(self, func, fps):
		animator = Animator(func, fps)
		return animator
class Animator:
	def __init__(self, func, fps):
		self.delay = 1000 / fps
		self.func = func
		self.fcount = 0
		self.stopped = False
		thread = Thread(None, self.doit)
		thread.daemon = True
		thread.start()
	def stop(self): self.stopped = True
	def doit(self):
		while True:
			if self.stopped: return
			frame_start = time_ns()
			self.func()
			frame_end = time_ns()
			wait_ms = self.delay - (frame_end - frame_start) / 1000000
			if wait_ms <= 0: wait_ms = 0
			sleep(wait_ms / 1000)
if __name__ == '__main__':
	from random import randint
	def paint():
		draw.fill('red')
		draw.rect(randint(0, 290), randint(0, 290), 10, 10)
	window = Tk()
	draw = EasyCanvas(300, 300)
	draw.fill('black')
	draw.text('this sucks', 100, 100)
	draw.grid()
	draw.animate(paint, 30)
	window.mainloop()