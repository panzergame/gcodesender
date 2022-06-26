import sdl2
import time


class Joystick:
	MAX_AXIS_VAL = 32767
	AXIS_FORMAT = '{}{:.5f}'
	MOVE_CMD = 'G91 G0 {} G4 P0'
	ABSOLUTE_CMD = 'G90'

	def __init__(self, config, controller):
		self._config = config
		self._axes_config = self._config['axes']
		self._controller = controller

		self._mapping = [sdl2.SDL_GameControllerGetAxisFromString(axis['mapping'].get().encode()) for axis in self._axes_config.values()]
		self._exit_mapping = sdl2.SDL_GameControllerGetButtonFromString(self._config['exit']['mapping'].get().encode())

		self._init_gamecontroller()

	def _init_gamecontroller(self):
		status = sdl2.SDL_Init(sdl2.SDL_INIT_GAMECONTROLLER)
		assert(sdl2.SDL_GameControllerAddMappingsFromFile(b'src/gcodesender/interactive/gamecontrollerdb.txt') != -1)

		index = self._config['index'].get(int)
		self._gamecontroller = sdl2.SDL_GameControllerOpen(index)
		name = sdl2.SDL_GameControllerNameForIndex(index)

		self._attached = sdl2.SDL_GameControllerGetAttached(self._gamecontroller)
		if self._attached:
			print(f'Connected to joystick {name.decode()}')
		else:
			print(f'Failed to connect to joystick at index {index}')

	def _move(self, axes: [str]):
		cmd = self.MOVE_CMD.format(' '.join(self.AXIS_FORMAT.format(name, dist) for name, dist in axes.items()))
		print(cmd)
		self._controller.send_command(cmd)

	def _check_axis(self):
		axes = {}
		for (name, axis), mapping in zip(self._axes_config.items(), self._mapping):
			val = sdl2.SDL_GameControllerGetAxis(self._gamecontroller, mapping) / self.MAX_AXIS_VAL
			val_exp = val ** 3
			if abs(val_exp) > axis['threshold'].get(float):
				invert_coeff = -1 if axis['invert'].get(bool) else 1
				dist = val_exp * axis['step'].get(float) * invert_coeff
				axes[name] = dist
		if len(axes) > 0:
			self._move(axes)

	def _check_exit(self) -> bool:
		pressed = sdl2.SDL_GameControllerGetButton(self._gamecontroller, self._exit_mapping)
		return pressed == 0

	def _reset_absolute(self):
		self._controller.send_command(self.ABSOLUTE_CMD)

	def run(self):
		sdl2.SDL_GameControllerUpdate()

		while self._check_exit():
			time.sleep(0.01)
			self._check_axis()
			sdl2.SDL_GameControllerUpdate()

		self._reset_absolute()
