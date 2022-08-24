# GCode Sender

Gcode Sender is a tool that allows GRBL users to send GCode from file or from interactive command interface.

## Features

* Stream any file with GRBL supported commands
* Interactive command interface for homing before sending file
* Joystick control for homing

## Installation

Run pip to install dependencies:

```sh
pip3 install -r requirements.txt
```

## Usage

A typical usage looks like:
```sh
python3 -m src.gcodesender /dev/ttyUSB0 -s -c -f piece.ngc
```

`/dev/ttyUSB0` stands for your USB serial and `-f piece.ngc` for your gcode command file. Options `-s -c` allows to enter an interactive command interface for homing before sending file, it can be exited with command `co` or Ctrl+D to continue.

In order to use a joystick to move head for homing before cut replace option `-c` by `-j`. Joystick configuration can be overwritten at .config/gcodesender/config.yaml with following default values :

```yaml
joystick:
  index: 0
  axes:
    x:
      threshold: 0.01
      step: 0.1
      mapping: rightx
      invert: no
    y:
      threshold: 0.01
      step: 0.05
      mapping: lefty
      invert: no
    z:
      threshold: 0.01
      step: 0.1
      mapping: righty
      invert: no
  exit:
    mapping: a
```

## 🤝 Contributing

Contributions, issues and feature requests are welcome!<br />Feel free to check [issues page](https://github.com/panzergame/gcodesender/issues). 

## Show your support

Give a ⭐️ if this project helped you!

## 📝 License

Copyright © 2020 [Tristan Porteries](https://github.com/panzergame).<br />
This project is [MIT License](https://github.com/panzergame/gcodesender/blob/master/LICENSE.md) licensed.
