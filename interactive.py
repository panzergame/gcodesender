import cmd


class Interactive(cmd.Cmd):
	intro = """Welcome to Gcode interactive console.
Type any command then continue to next stage with 'co'"""
	prompt = "(gcs) "

	def __init__(self, controller):
		cmd.Cmd.__init__(self)
		self.controller = controller

	def do_co(self, line):
		return True

	def do_EOF(self, line):
		return True

	def default(self, line):
		"""Handle default commands, send them to grbl
		"""
		res = self.controller.send_command(line)
		print(res)
