import cmd


class Console(cmd.Cmd):
	intro = """Welcome to Gcode interactive console.
Type any command then continue to next stage with 'co' or Ctrl+D"""
	prompt = "(gcs) "

	def __init__(self, controller, inspector):
		cmd.Cmd.__init__(self)
		self._controller = controller
		self.doRepeat = False
		self._inspector = inspector

	def do_co(self, line):
		return True

	def do_EOF(self, line):
		return True

	def do_re(self, line):
		self.doRepeat = True
		return True

	def do_te(self, plane):
		if self._inspector is None:
			print('No file selected')
			return

		gcodes = self._inspector.bounding_rect_gcodes
		if gcodes is None:
			print('Missing metadata gcodes')
			return

		self._controller.reset_origin()
		self._controller.send_commands(self._inspector.bounding_rect_gcodes)

	def do_help(self, line):
		self.default(line)

	def default(self, line):
		"""Handle default commands, send them to grbl
		"""
		response = self._controller.send_command(line)
		for line in response:
			print(line)
