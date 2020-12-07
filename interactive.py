import cmd


class Interactive(cmd.Cmd):
	intro = """Gcode interpreter.
type any command then continue to next stage with 'co'"""
	prompt = "(gcs) "

	def __init__(self, serial):
		cmd.Cmd.__init__(self)
		self.serial = serial

	def do_co(self, line):
		return True

	def do_EOF(self, line):
		return True

	def default(self, line):
		"""Handle default commands, send them to grbl
		"""
		try:
			res = self.serial.send_wait_command(line)
			print(res)
		except ValueError as exception:
			cmd, res = exception.args
			print("Invalid command: {}, error code: {}".format(cmd, res))
