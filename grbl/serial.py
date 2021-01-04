import serial
import re
import time


class Serial:
	def __init__(self, device, baudrate):
		self.pipe = serial.Serial(device, baudrate)

	def __enter__(self):

		# Wait for grbl to print welcome messages
		time.sleep(2)

		# Clear all input/output
		self.pipe.reset_input_buffer()
		self.pipe.reset_output_buffer()

		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.pipe.close()

	def _read_line(self):
		"""Read (blocking) a line from grbl and strip whitespaces
		"""
		return self.pipe.readline().decode().strip()

	def _read_lines_untils(self, terminator_regex):
		"""Read all lines until a terminator regex match a line and return all read lines
		"""

		terminator_match_prog = re.compile(terminator_regex)

		lines = []
		line = self._read_line()
		while not terminator_match_prog.match(line):
			lines.append(line)
			line = self._read_line()

		# Insert last line matching terminator
		lines.append(line)

		self.pipe.reset_input_buffer()

		return lines

	def send_wait_command(self, cmd):
		"""Send a gcode command and wait for response from grbl
		"""
		self.pipe.write((cmd + "\r\n").encode())

		res = "\n".join(self._read_lines_untils("^(ok|error).*"))

		if res.startswith("error"):
			raise ValueError(cmd, res)

		return res
