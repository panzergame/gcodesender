import cmd


class Console(cmd.Cmd):
	intro = """Welcome to Gcode interactive console.
Type any command then continue to next stage with 'co' or Ctrl+D"""
	prompt = "(gcs) "

	def __init__(self, controller):
		cmd.Cmd.__init__(self)
		self.controller = controller
		self.doRepeat = False

	def do_co(self, line):
		return True

	def do_EOF(self, line):
		return True

	def do_re(self, line):
		self.doRepeat = True
		return True

	def do_help(self, line):
		self.default(line)

	def default(self, line):
		"""Handle default commands, send them to grbl
		"""
		response = self.controller.send_command(line)
		for line in response:
			print(line)
