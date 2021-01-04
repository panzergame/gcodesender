class Controller:
	UNLOCK_CMD = "$x"
	RESET_ORIGIN_CMD = "G92 X0 Y0 Z0"

	def __init__(self, serial):
		self.serial = serial

	def send_file(self, filename):
		"""Send file content line by line as commands
		Wait until all commands are send or an error is detected
		"""

		try:
			print("Sending file {}".format(filename))

			with open(filename, "r") as file:
				# Strip all lines
				lines = map(lambda line: line.strip(), file)
				for line in lines:
					# Send command and wait for grbl to accept
					res = self.serial.send_wait_command(line)
					print(res)

		except ValueError as exception:
			cmd, res = exception.args
			print("Invalid command: {}, error code: {}".format(cmd, res))

	def send_command(self, cmd):
		"""Send a gcode command and wait for response from grbl
		"""
		try:
			return self.serial.send_wait_command(cmd)
		except ValueError as exception:
			cmd, res = exception.args
			print("Invalid command: {}, error code: {}".format(cmd, res))

	def unlock(self):
		"""Unlock grbl for sending move commands
		"""
		self.send_command(self.UNLOCK_CMD)

	def reset_origin(self):
		"""Reset coordinate origin to (0, 0, 0)
		"""
		self.send_command(self.RESET_ORIGIN_CMD)
