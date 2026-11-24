import cmd
import readline
from prompt_toolkit import PromptSession


class Console(cmd.Cmd):
    intro = """Welcome to Gcode interactive console.
Type any command then continue to next stage with 'co' or Ctrl+D"""
    prompt = "(gcs) "

    def __init__(self, controller, inspector):
        cmd.Cmd.__init__(self)
        self._controller = controller
        self.doRepeat = False
        self._inspector = inspector
        self._session = PromptSession()

    def cmdloop(self, intro=None):
        # cmd.Cmd calls input() directly, so the loop has to be replaced
        # to read lines through prompt_toolkit.
        self.preloop()
        print(intro or self.intro)
        stop = False
        while not stop:
            try:
                line = self._session.prompt(self.prompt)
            except EOFError:
                line = 'EOF'
            line = self.precmd(line)
            stop = self.onecmd(line)
            stop = self.postcmd(stop, line)
        self.postloop()

    def do_co(self, line):
        return True

    def do_EOF(self, line):
        return True

    def do_x(self, line):
        print('Resetting...')
        self._controller.reset()

    def do_re(self, line):
        self.doRepeat = True
        return True

    def do_te(self, plane):
        if self._inspector is None:
            print('No file selected')
            return

        gcodes = self._inspector.bounding_rect_gcodes
        if gcodes is None:
            print('Missing metadata gcodes')
            return

        self._controller.reset_origin()
        self._controller.send_commands(self._inspector.bounding_rect_gcodes)

    def do_help(self, line):
        self.default(line)

    def default(self, line):
        """Handle default commands, send them to grbl
        """
        self._controller.send_command(line)
