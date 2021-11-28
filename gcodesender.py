import argparse
import grbl
from interactive import Interactive


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-s", "--start-console", action="store_true")
	parser.add_argument("-e", "--end-console", action="store_true")
	parser.add_argument("device")
	parser.add_argument("-f", "--filename")
	parser.add_argument("-b", "--baudrate", type=int, default=115200)

	args = parser.parse_args()

	with grbl.Serial(args.device, args.baudrate) as serial:
		controller = grbl.Controller(serial)
		controller.unlock()

		try:
			if args.start_console:
				inter = Interactive(controller)
				inter.cmdloop()

			doRun = True
			while doRun:
				controller.reset_origin()
				if "filename" in args:
					controller.send_file(args.filename)

				if args.end_console:
					inter = Interactive(controller)
					inter.cmdloop()
					doRun = inter.doRepeat
				else:
					doRun = False
		except KeyboardInterrupt:
			controller.stop()
