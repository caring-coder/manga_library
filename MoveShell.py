import cmd
import os
import shutil


class MoveShell (cmd.Cmd):

    def __init__(self, source_path, target_path, force=False):
        super(MoveShell, self).__init__()
        self.force = force
        self.source_path = source_path
        self.target_path = target_path
        self.prompt = 'Move ? yn '
        self.do_nothing = lambda: None

    def do_y(self, arg):
        if self.force:
            os.makedirs(os.path.dirname(self.target_path), exist_ok=True)
            shutil.move(self.source_path, self.target_path + "_temp")
            os.removedirs(self.target_path)
            shutil.move(self.target_path + "_temp", self.target_path)
            return True

        if os.path.exists(self.target_path):
            print(self.target_path + " already exists")
            exit(5)

        os.makedirs(os.path.dirname(self.target_path), exist_ok=True)
        shutil.move(self.source_path, self.target_path)
        return True

    def do_n(self, arg):
        self.do_nothing()
        return True

    def do_exit(self, arg):
        self.do_nothing()
        exit(3)

    def emptyline(self):
        return self.do_y(None)
