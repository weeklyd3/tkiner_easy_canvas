from tkinter import *
DEFAULT_CONFIG = {
	'fill': 'black',
	'stroke': '',
	'translate': [0, 0]
}
class Config:
	def __init__(self, parent, config = {}):
		self.config = config
		self.parent = parent
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

	# wrappers around canvas.create_* functions
	def rect(self, x, y, width, height):
		self.create_rectangle(
			*self._coordinates([x, y]),
			*self._coordinates([x + width, y + height]),
			fill = self._config.get('fill'),
			outline = self._config.get('stroke')
		)
if __name__ == '__main__':
	window = Tk()
	draw = EasyCanvas(300, 300)
	draw.grid()
	draw.fill('red')
	draw.translate(100, 100)
	draw.rect(0, 0, 100, 100)
	window.mainloop()