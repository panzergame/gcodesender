import serial
import re
import time


class Serial:
    def __init__(self, device, baudrate):
        self._pipe = serial.Serial(device, baudrate)
        self._ok_or_error_regex_prog = re.compile("^(ok|error|ALARM).*")

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
        while True:
            line = self._read_line()
            lines.append(line)

            if match := terminator_regex_prog.match(line):
                self._pipe.reset_input_buffer()
                return lines, match.group(1)

    def send_wait_command(self, cmd: str) -> [str]:
        """Send a gcode command and wait for response from grbl
        """
        self.send_command(cmd)

        received_lines, terminator_match = self._read_lines_untils(
            self._ok_or_error_regex_prog)

        if terminator_match in ('error', 'ALARM'):
            raise ValueError(cmd, received_lines)

        return received_lines

    def send_command(self, cmd: str):
        """Send a gcode command
        """
        self._pipe.write((cmd + "\r\n").encode())


class StubSerial:
    def __init__(self, device, baudrate):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def _read_line(self) -> str:
        return ''

    def _read_lines_untils(self, terminator_regex_prog: re.Pattern):
        return []

    def send_wait_command(self, cmd: str) -> [str]:
        return ['ok']

    def send_command(self, cmd: str):
        pass
