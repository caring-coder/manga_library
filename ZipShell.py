import cmd
import os
import shutil


class ZipShell (cmd.Cmd):

    def __init__(self, source_path, target_path):
        super(ZipShell, self).__init__()
        self.source_path = source_path
        self.target_path = target_path
        self.prompt = 'Zip ? yn '
        self.do_nothing = lambda: None

    def do_y(self, arg):
        if not os.path.isdir(self.source_path):
            print(self.source_path + " is not a valid directory")
            exit(4)
        root_name = os.path.dirname(self.source_path)
        base_name = os.path.basename(self.source_path)
        shutil.make_archive(self.target_path, 'zip', root_name, base_name)
        shutil.move(self.target_path + '.zip', self.target_path)
        return True

    def do_n(self, arg):
        self.do_nothing()
        return True

    def do_exit(self, arg):
        self.do_nothing()
        exit(8)

    def emptyline(self):
        return self.do_y(None)
