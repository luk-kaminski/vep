#!/usr/bin/env python3

import io
import sys


def top_lines_to_new_file(original_fname, new_fname, limit):
    original_file = io.open(original_fname, 'r', encoding='utf-8', newline='\n')
    new_file = io.open(new_fname, 'w', encoding='utf-8', newline='\n')
    if original_fname.endswith('.vec'):
        n, d = map(int, original_file.readline().split())
        # do nothing with this line
    for line in original_file:
        new_file.write(line)
        limit -= 1
        if limit <= 0:
            break


if __name__ == "__main__":
    file_name = sys.argv[1]
    extension = file_name[file_name.rindex('.'):]
    limit = sys.argv[2]
    new_file_name_ending = '-cut-to-' + limit + extension
    new_file_name = file_name.replace(extension, new_file_name_ending)
    top_lines_to_new_file(file_name, new_file_name, int(limit))
