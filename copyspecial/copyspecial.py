#!/usr/bin/python3
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import os
import shutil
import subprocess

"""Copy Special exercise
"""

def get_special_paths(dir):
  """
  returns a list of the absolute paths of the special files in the given directory
  """
  special_files = []
  cwd = os.getcwd()
  files = os.listdir(dir)
  for file in files:
    m = re.search(r"__\w+__", file)
    if m:
      special_files.append(os.path.join(cwd, dir, file))
  return special_files

def copy_to(paths, dir):
  """
  given a list of paths, copies those files into the given directory
  """
  if not os.path.exists(dir):
    os.mkdir(dir)

  for path in paths:
    shutil.copy(path, dir)


def main():
  # This basic command line argument parsing code is provided.
  # Add code to call your functions below.

  # Make a list of command line arguments, omitting the [0] element
  # which is the script itself.
  args = sys.argv[1:]
  if not args:
    print('usage: [--todir dir][--tozip zipfile] dir [dir ...]')
    sys.exit(1)

  # todir and tozip are either set from command line
  # or left as the empty string.
  # The args array is left just containing the dirs.
  dst_dir = os.path.join(os.getcwd(), 'out') 
  if args[0] == '--todir':
    dst_dir = args[1]
    del args[0:2]

  dst_zip = os.path.join(os.getcwd(), 'out')
  if args[0] == '--tozip':
    dst_zip = args[1]
    del args[0:2]

  if not args: # A zero length array evaluates to "False".
    print('error: must specify one or more dirs')
    sys.exit(1)

  for src_dir in args:
    paths = get_special_paths(src_dir)
    copy_to(paths, dst_dir)
  shutil.make_archive(dst_zip, 'zip', dst_dir)

if __name__ == '__main__':
  main()
