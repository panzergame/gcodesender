# GCode Sender

Gcode Sender is a tool that allows GRBL users to send GCode from file or from interactive command interface.

## Features

* Stream any file with GRBL supported commands
* Interactive command interface for homing before sending file

## Installation

This project depends on pyserial, it can be installed using pip:

```sh
pip3 install pyserial
```

## Usage

A typical usage looks like:
```sh
python3 gcodesender.py /dev/ttyUSB0 -s -f piece.ngc
```

`/dev/ttyUSB0` stands for your USB serial and `-f piece.ngc` for your gcode command file. Options `-s` allows to enter an interactive command interface for homing before sending file, it can be exited with command `co` or Ctrl+D to continue.


## 🤝 Contributing

Contributions, issues and feature requests are welcome!<br />Feel free to check [issues page](https://github.com/panzergame/gcodesender/issues). 

## Show your support

Give a ⭐️ if this project helped you!

## 📝 License

Copyright © 2020 [Tristan Porteries](https://github.com/panzergame).<br />
This project is [MIT License](https://github.com/panzergame/gcodesender/blob/master/LICENSE.md) licensed.
