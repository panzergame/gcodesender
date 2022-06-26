import argparse
from .config import config
from . import grbl
from .interactive.console import Console
from .interactive.joystick import Joystick

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

	with grbl.Serial(args.device, args.baudrate) as serial:
		controller = grbl.Controller(serial)
		controller.unlock()

		def run_interactive_session() -> bool:
			if args.use_console:
				console = Console(controller)
				console.cmdloop()
				doRepeat = console.doRepeat
			if args.use_joystick:
				joystick = Joystick(config['joystick'], controller)
				joystick.run()
				doRepeat = False
			return doRepeat

		try:
			if args.start_interactive_session:
				run_interactive_session()

			doRun = True
			while doRun:
				controller.reset_origin()
				if "filename" in args:
					controller.send_file(args.filename)

				doRun = run_interactive_session() if args.end_interactive_session else False
		except KeyboardInterrupt:
			controller.stop()

