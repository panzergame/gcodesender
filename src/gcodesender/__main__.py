import argparse
from .config import config
from . import grbl
from .interactive.console import Console
from .interactive.joystick import Joystick

class Scenario:
	def __init__(self, args):
		self.args = args
		self.inspector = grbl.GCodeInspector(self.args.filename) if self.args.filename else None

	def run_file_step(self):
		self.controller.reset_origin()
		if "filename" in self.args:
			self.controller.send_file(self.args.filename)


	def run_one_cycle(self):
		self.run_file_step()
		doRun = self.run_interactive_session() if self.args.end_interactive_session else False
		return doRun


	def run_cycles(self):
		while self.run_one_cycle():
			pass


	def run_interactive_session(self) -> bool:
		if self.args.use_console:
			console = Console(self.controller, self.inspector)
			console.cmdloop()
			doRepeat = console.doRepeat
		if self.args.use_joystick:
			joystick = Joystick(config['joystick'], self.controller, self.inspector)
			joystick.run()
			doRepeat = False
		return doRepeat


	def run(self):
		with grbl.Serial(args.device, args.baudrate) as serial:
			self.controller = grbl.Controller(serial)
			self.controller.unlock()

			try:
				if self.args.start_interactive_session:
					self.run_interactive_session()

				self.run_cycles()

			except KeyboardInterrupt:
				self.controller.stop()


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-c", "--use-console", action="store_true")
	parser.add_argument("-j", "--use-joystick", action="store_true")
	parser.add_argument("-s", "--start-interactive-session", action="store_true")
	parser.add_argument("-e", "--end-interactive-session", action="store_true")
	parser.add_argument("device")
	parser.add_argument("-f", "--filename")
	parser.add_argument("-b", "--baudrate", type=int, default=115200)

	args = parser.parse_args()

	scenario = Scenario(args)
	scenario.run()


