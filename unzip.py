import argparse
import os
import shutil
import zipfile


def check_that_dir_contains_only_one_letter_dirs(path: str) -> list:
    sub_directories = os.listdir(path)
    sub_directories.sort()
    sub_paths = []

    for sub_directory in sub_directories:
        # print(sub_directory)
        sub_path = os.path.join(path, sub_directory)
        if not os.path.isdir(sub_path):
            print("This node '" + sub_directory + "' is not a directory.")
            return sub_paths

        if len(sub_directory) > 1:
            print("This node '" + sub_directory + "' has a too long name.")
            return sub_paths

        sub_paths.append(sub_path)
    return sub_paths


def check_that_dir_contains_only_dirs(path: str) -> list:
    sub_directories = os.listdir(path)
    sub_directories.sort()
    sub_paths = []

    for sub_directory in sub_directories:
        # print(sub_directory)
        sub_path = os.path.join(path, sub_directory)
        if not os.path.isdir(sub_path):
            print("This node '" + sub_directory + "' is not a directory.")
            return sub_paths
        sub_paths.append(sub_path)
    return sub_paths


def check_that_dir_contains_only_zip(path: str) -> list:
    sub_directories = os.listdir(path)
    sub_directories.sort()
    sub_paths = []

    for sub_directory in sub_directories:
        # print(sub_directory)
        sub_path = os.path.join(path, sub_directory)
        if not zipfile.is_zipfile(sub_path):
            print("This node '" + sub_path + "' is not zip file.")
            continue
        sub_paths.append(sub_path)
    return sub_paths


def check_that_zip_contains_only_one_folder(path: str) -> str:
    with zipfile.ZipFile(path, 'r') as my_zip:
        zip_folder_entries = [zip_entry for zip_entry in my_zip.infolist() if zip_entry.filename.endswith("/")]
        if len(zip_folder_entries) != 1:
            print("This zip '" + path + "' contains more than one entry.")
    return path


def check_that_fullpath_does_not_contains_a_language(path: str) -> str:
    if "(english)" in path.lower():
        print("This path '" + path + "' contains a language reference.")
    return path


def unzip_and_delete(path: str):
    print("unzipping " + path)
    shutil.unpack_archive(path, os.path.dirname(path), 'zip')
    print("deleting " + path)
    os.remove(path)


def apply(f: callable, elements: list) -> list:
    aggregate = []
    for element in elements:
        result = f(element)
        if result:
            aggregate.extend(result)
    return aggregate


parser = argparse.ArgumentParser()
parser.add_argument('--path', default='/data/NSFW/comic')
args = parser.parse_args()

letters_root = args.path

authors_roots = check_that_dir_contains_only_one_letter_dirs(letters_root)
books_root = apply(check_that_dir_contains_only_dirs, authors_roots)
book_paths = apply(check_that_dir_contains_only_zip, books_root)
valid_books = apply(check_that_fullpath_does_not_contains_a_language, book_paths)
valid_books = apply(check_that_zip_contains_only_one_folder, book_paths)
