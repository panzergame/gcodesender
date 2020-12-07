import argparse
from grblserial import GrblSerial
from interactive import Interactive


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-s", "--start-console", action="store_true")
	parser.add_argument("-e", "--end-console", action="store_true")
	parser.add_argument("device")
	parser.add_argument("-f", "--filename")
	parser.add_argument("-b", "--baudrate", type=int, default=115200)

	args = parser.parse_args()

	with GrblSerial(args.device, args.baudrate) as serial:
		serial.unlock()

		if args.start_console:
			inter = Interactive(serial)
			inter.cmdloop()

		serial.reset_origin()
		if "filename" in args:
			serial.send_file(args.filename)

		if args.end_console:
			inter = Interactive(serial)
			inter.cmdloop()
