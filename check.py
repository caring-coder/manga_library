#!/usr/bin/env python3

import argparse
import os
import re
from MoveShell import MoveShell
from RemoveShell import RemoveShell
from ZipShell import ZipShell
import zipfile
import rarfile
import shutil


def compute_target_path_for_file(name):
    first_letter = name[0]
    artist_name = name.split(',')[0]
    return os.path.join(first_letter, artist_name, name)


def remove_dir_if_empty(dir_path):
    if not os.path.isdir(dir_path):
        return

    zip_content = os.listdir(dir_path)
    if len(zip_content) == 0:
        shell_prompt_template = "Remove {0} ? it seems to be empty."
        shell_prompt = shell_prompt_template.format(dir_path)
        RemoveShell(dir_path).cmdloop(shell_prompt)


def check_letter_directory(dir_path):
    author_directories = os.listdir(dir_path)
    author_directories.sort()
    if len(author_directories) == 0:
        print("This directory '" + dir_path + "' is empty.")
        os.rmdir(dir_path)

    for author_directory in author_directories:
        print("│ ├─┐ " + author_directory)
        author_directory_path = os.path.join(dir_path, author_directory)
        if not os.path.isdir(author_directory_path):
            filename = os.path.basename(author_directory_path)
            subtarget_path = compute_target_path_for_file(filename)
            target_path = os.path.join(root, subtarget_path)
            MoveShell(author_directory_path, target_path).cmdloop("Move " + filename + " to " + subtarget_path + " ?")
            continue

        if not author_directory.startswith(letter_directory):
            target_path = os.path.join(root, letter_directory, author_directory)
            MoveShell(author_directory_path, target_path).cmdloop(
                "Move " + author_directory + " to " + target_path + " ?")
            continue

        if re.match("^[^([]+,.*$", author_directory):
            target_path = os.path.join(root, letter_directory, author_directory.split(",")[0], author_directory)
            MoveShell(author_directory_path, target_path).cmdloop(
                "Move " + author_directory + " to " + target_path + " ?")
            continue

        check_author_directory(author_directory_path)


def check_author_directory(author_directory_path):
    books_files = os.listdir(author_directory_path)
    books_files.sort()

    while len(books_files) > 0:
        book_file = books_files.pop(0)

        if len(books_files) > 0:
            print("│ │ ├─ " + book_file)
        else:
            print("│ │ └─ " + book_file)

        zip_file_path = os.path.join(author_directory_path, book_file)

        if os.path.isfile(zip_file_path):
            if rarfile.is_rarfile(zip_file_path):
                print(zip_file_path + " is a rar.")
                with rarfile.RarFile(zip_file_path) as my_rar:
                    my_rar.extractall(os.path.splitext(zip_file_path)[0])
                os.remove(zip_file_path)
                continue

            if zip_file_path.endswith("Hentairules.net, Zip English Hentai.url"):
                os.remove(zip_file_path)
                print(zip_file_path + " is not a zip.")
                continue

            if zip_file_path.endswith("notes and info from the uploader.txt"):
                os.remove(zip_file_path)
                print(zip_file_path + " is not a zip.")
                continue

            if zip_file_path.endswith("that file comes from hentairules.net.txt"):
                os.remove(zip_file_path)
                print(zip_file_path + " is not a zip.")
                continue

            if zip_file_path.endswith("notes and info from hentairules.net.txt"):
                os.remove(zip_file_path)
                print(zip_file_path + " is not a zip.")
                continue

            if zip_file_path.endswith("hentairulesbanner.png"):
                os.remove(zip_file_path)
                print(zip_file_path + " is not a zip.")
                continue

            if zip_file_path.endswith("hentairulesbanner.jpg"):
                os.remove(zip_file_path)
                print(zip_file_path + " is not a zip.")
                continue

            if zip_file_path.endswith(".pdf"):
                continue

            if not zipfile.is_zipfile(zip_file_path):
                print(zip_file_path + " is not a zip.")
                continue

            with zipfile.ZipFile(zip_file_path, 'r') as my_zip:
                nb_dir = 0
                nb_url = 0
                nb_png = 0
                nb_entry = 0
                nb_txt = 0
                nb_jpg = 0
                nb_gif = 0
                for info in my_zip.infolist():
                    nb_entry = nb_entry + 1
                    if info.filename.endswith("/"):
                        nb_dir = nb_dir + 1
                    if info.filename.endswith(".url"):
                        nb_url = nb_url + 1
                    if info.filename.endswith(".png"):
                        nb_png = nb_png + 1
                    if info.filename.endswith(".txt"):
                        nb_txt = nb_txt + 1
                    if info.filename.endswith(".html"):
                        nb_txt = nb_txt + 1
                    if info.filename.endswith(".nfo"):
                        nb_txt = nb_txt + 1
                    if info.filename.endswith(".jpg"):
                        nb_jpg = nb_jpg + 1
                    if info.filename.endswith(".JPG"):
                        nb_jpg = nb_jpg + 1
                    if info.filename.endswith(".jpeg"):
                        nb_jpg = nb_jpg + 1
                    if info.filename.endswith(".gif"):
                        nb_gif = nb_gif + 1

                if nb_dir > 1:
                    shutil.unpack_archive(zip_file_path, os.path.dirname(zip_file_path), 'zip')
                    os.remove(zip_file_path)
                    print("This zip '" + zip_file_path + "' contains several dirs.")
                    continue

                if nb_entry > nb_dir + nb_url + nb_png + nb_txt + nb_jpg + nb_gif:
                    print("This zip '" + zip_file_path + "' contains files not authorized")
                    shutil.unpack_archive(zip_file_path, os.path.dirname(zip_file_path), 'zip')
                    os.remove(zip_file_path)
                    exit(10)

                if nb_dir == 0:
                    shutil.unpack_archive(zip_file_path, os.path.splitext(zip_file_path)[0], 'zip')
                    os.remove(zip_file_path)
                    print("This zip '" + zip_file_path + "' contains no dirs.")
                    continue

                if nb_url > 3:
                    print("This zip '" + zip_file_path + "' contains several url files")
                    exit(10)

            continue

        if os.path.isdir(zip_file_path):

            dir_content = list(os.scandir(zip_file_path))
            if len(dir_content) == 1 and dir_content[0].is_dir():
                print("This node '" + zip_file_path + "' contains only one dir.")
                filename = os.listdir(zip_file_path)[0]
                source_path = os.path.join(zip_file_path, filename)
                target_path = os.path.join(author_directory_path, filename)
                MoveShell(source_path, target_path, force=True).cmdloop("Move " + filename + " to " + target_path + " ?")
            else:
                for entry in dir_content:
                    if entry.is_dir():
                        print("This node '" + zip_file_path + "' contains a dir.")
                        exit(6)

            nb_files = len(os.listdir(zip_file_path))
            if nb_files == 1:
                print("This node '" + zip_file_path + "' contains only one file.")
                filename = os.listdir(zip_file_path)[0]
                source_path = os.path.join(zip_file_path, filename)
                target_path = os.path.join(author_directory_path, filename)
                MoveShell(source_path, target_path).cmdloop("Move " + filename + " to " + target_path + " ?")
            elif nb_files > 1:
                ZipShell(zip_file_path, zip_file_path + '.cbz').do_y(None)
                RemoveShell(zip_file_path).do_y(None)
                continue

            remove_dir_if_empty(zip_file_path)


parser = argparse.ArgumentParser()
parser.add_argument('--path', default='/data/NSFW/comic')
args = parser.parse_args()

root = args.path

letter_directories = os.listdir(args.path)
letter_directories.sort()

for letter_directory in letter_directories:
    currentDirectory = os.path.join(root, letter_directory)
    print("├─┐" + letter_directory)
    if not os.path.isdir(currentDirectory):
        print("This node '" + letter_directory + "' is not a directory.")
        exit(1)

    if len(letter_directory) > 1:
        print("This directory '" + letter_directory + "' has a too long name.")
        exit(2)

    check_letter_directory(currentDirectory)








