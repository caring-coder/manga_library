import cmd
import os
import shutil


class RemoveShell (cmd.Cmd):

    def __init__(self, source_path):
        super(RemoveShell, self).__init__()
        self.source_path = source_path
        self.prompt = 'Remove ? yn '
        self.do_nothing = lambda: None

    def do_y(self, arg):
        if not os.path.isdir(self.source_path):
            print(self.source_path + " is not a valid directory")
            exit(4)

        shutil.rmtree(self.source_path)
        return True

    def do_n(self, arg):
        self.do_nothing()
        return True

    def do_exit(self, arg):
        self.do_nothing()
        exit(7)

    def emptyline(self):
        return self.do_y(None)
