class Controller:
	UNLOCK_CMD = '$x'
	RESET_ORIGIN_CMD = 'G92 X0 Y0 Z0'
	STOP_CMD = '!'

	def __init__(self, serial):
		self.serial = serial

	def send_file(self, filename: str):
		"""Send file content line by line as commands
		Wait until all commands are send or an error is detected
		"""
		print(f'Sending file {filename}')

		with open(filename, "r") as file:
			# Strip all lines
			lines = [line.strip() for line in file]
			total_lines = len(lines)
			try:
				for i, line in enumerate(lines):
					line_sent_percentage = (i + 1) / total_lines * 100
					print("[{:.0f}%] {}".format(line_sent_percentage, line))

					# Send command and wait for grbl to accept
					response = self.serial.send_wait_command(line)
					for line in response:
						print(line)

			except ValueError as exception:
				cmd, res = exception.args
				print(f'Invalid command: {cmd}, error code: {res}')

	def stop(self):
		print('Stopping !')
		self.serial.send_command(self.STOP_CMD)

	def send_command(self, cmd: str) -> [str]:
		"""Send a gcode command and wait for response from grbl
		"""
		try:
			return self.serial.send_wait_command(cmd)
		except ValueError as exception:
			cmd, res = exception.args
			print(f'Invalid command: {cmd}, error code: {res}')
			return []

	def unlock(self):
		"""Unlock grbl for sending move commands
		"""
		self.send_command(self.UNLOCK_CMD)

	def reset_origin(self):
		"""Reset coordinate origin to (0, 0, 0)
		"""
		self.send_command(self.RESET_ORIGIN_CMD)
