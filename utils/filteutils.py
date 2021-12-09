"""
Utility functions.
"""
import csv
import os


def csv_open(file_name) -> list:
    """Read the given file name as a JSON entry and return it."""
    with open(file_name) as csvfile:
        return list(csv.DictReader(csvfile))


def text_open(file_name) -> list:
    """
    Read a text file and return a list of lines
    :return:
    :param file_name:
    :return:
    """
    with open(file_name, "r") as infile:
        return infile.readlines()


def exists(path):
    return os.path.exists(path)


def create_if_not_exists(*segments) -> str:
    full_path = build_full_path(*segments)
    os.makedirs(full_path, exist_ok=True)
    return full_path


def build_full_path(*segments) -> str:
    return os.path.expanduser(os.path.join(*segments))


def get_short_name(path: str) -> str:
    return os.path.basename(path)
