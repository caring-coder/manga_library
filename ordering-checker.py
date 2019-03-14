import argparse
import os

import regex as regex
from sortedcontainers import SortedDict


def find_valid_directories(dir_list, reg):
    valid_directories = SortedDict()
    for root, dirs in dir_list.items():
        for dir in dirs:
            dir_as_next_root = os.path.join(root, dir)
            if not regex.match(reg, dir):
                print(dir_as_next_root + " doesn't match the expression '" + reg.pattern + "'")
            else:
                valid_directories[dir_as_next_root] = sorted(os.listdir(dir_as_next_root))
    return valid_directories


parser = argparse.ArgumentParser()
parser.add_argument('--path', default='/data/NSFW/comic')
args = parser.parse_args()

root = args.path
dirs = SortedDict()
first_dirs = sorted(os.listdir(root))

if ".ordering-pattern" not in first_dirs:
    print("didn't found ordering checker")
    exit(1)
else:
    first_dirs.remove(".ordering-pattern")
dirs[root] = first_dirs

ordering_pattern_filepath = os.path.join(root, ".ordering-pattern")

with open(ordering_pattern_filepath) as pattern_file:
    for pattern in pattern_file.readlines():
        pattern_line = pattern.strip()
        reg = regex.compile(pattern_line)
        dirs = find_valid_directories(dirs, reg)




