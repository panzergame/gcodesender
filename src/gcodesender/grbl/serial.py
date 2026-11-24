import serial
import re
import time
import threading
from concurrent.futures import Future
from typing import Optional


class ResponseFuture:
    def __init__(self, terminating_regex):
        self._terminating_regex = terminating_regex
        self._lines = []
        self.future = Future()

    def new_line_received(self, line):
        self._lines.append(line)
        match = self._terminating_regex.match(line)

        if match:
            self.future.set_result((self._lines, match))
        return match is not None


class Serial:
    def __init__(self, device, baudrate):
        self._pipe = serial.Serial(device, baudrate, timeout=0.2)
        self._ok_or_error_regex_prog = re.compile("^(ok|error|ALARM|Grbl).*")

    def __enter__(self):

        # Wait for grbl to print welcome messages
        time.sleep(2)

        # Clear all input/output
        self._pipe.reset_input_buffer()
        self._pipe.reset_output_buffer()

        self._reader_stop_event = threading.Event()
        self._response_future = None
        self._reader = threading.Thread(target=self._reader_loop)
        self._reader.start()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._reader_stop_event.set()
        self._reader.join()
        self._pipe.close()

    def _reader_loop(self):
        while not self._reader_stop_event.is_set():
            line = self._read_line()
            if len(line) == 0:
                continue

            print(line)
            self._handle_new_line(line)

    def _handle_new_line(self, line):
        if self._response_future is None:
            return

        if self._response_future.new_line_received(line):
            self._response_future = None

    def _read_line(self) -> str:
        """Read (blocking) a line from grbl and strip whitespaces
        """
        try:
            return self._pipe.readline().decode().strip()
        except UnicodeDecodeError:
            return 'error: utf8-decode'

    def send_wait_command(self, cmd: str, eol: str) -> [str]:
        """Send a gcode command and wait for response from grbl
        """

        self._response_future = ResponseFuture(self._ok_or_error_regex_prog)
        self.send_command(cmd, eol)

        received_lines, terminator_match = self._response_future.future.result()

        if terminator_match.group(1) in ('error', 'ALARM'):
            raise ValueError(cmd, received_lines)
        return received_lines

    def send_command(self, cmd: str, eol: str):
        """Send a gcode command
        """
        self._pipe.write((cmd + eol).encode())


class StubSerial:
    def __init__(self, device, baudrate):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def _read_line(self) -> str:
        return ''

    def send_wait_command(self, cmd: str, eol: str) -> [str]:
        return ['ok']

    def send_command(self, cmd: str, eol: str):
        pass
