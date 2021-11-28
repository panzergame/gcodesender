import serial
import re
import time


class Serial:
	def __init__(self, device, baudrate):
		self._pipe = serial.Serial(device, baudrate)
		self._ok_or_error_regex_prog = re.compile("^(ok|error).*")

	def __enter__(self):

		# Wait for grbl to print welcome messages
		time.sleep(2)

		# Clear all input/output
		self._pipe.reset_input_buffer()
		self._pipe.reset_output_buffer()

		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		self._pipe.close()

	def _read_line(self) -> str:
		"""Read (blocking) a line from grbl and strip whitespaces
		"""
		return self._pipe.readline().decode().strip()

	def _read_lines_untils(self, terminator_regex_prog: re.Pattern):
		"""Read all lines until a terminator regex match a line and return all read lines
		"""

		lines = []
		line = self._read_line()
		while not terminator_regex_prog.match(line):
			lines.append(line)
			line = self._read_line()

		# Insert last line matching terminator
		lines.append(line)

		self._pipe.reset_input_buffer()

		return lines

	def send_wait_command(self, cmd: str) -> [str]:
		"""Send a gcode command and wait for response from grbl
		"""
		self.send_command(cmd)

		received_lines = self._read_lines_untils(self._ok_or_error_regex_prog)

		first_received_line = received_lines[0]
		if first_received_line.startswith("error"):
			raise ValueError(cmd, first_received_line)

		return received_lines

	def send_command(self, cmd: str):
		"""Send a gcode command
		"""
		self._pipe.write((cmd + "\r\n").encode())
