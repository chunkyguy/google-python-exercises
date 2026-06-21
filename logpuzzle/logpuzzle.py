#!/usr/bin/python3
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib.parse
import urllib.request

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""


def read_urls(filename):
  """Returns a list of the puzzle urls from the given log file,
  extracting the hostname from the filename itself.
  Screens out duplicate urls and returns the urls sorted into
  increasing order."""
  file = open(filename, 'rt')
  contents = file.read()
  file.close()
  matches = re.findall(r"GET (\S+\/puzzle\/\S+)", contents)
  urls = []
  for match in matches:    
    url = urllib.parse.urljoin('https://code.google.com', match)
    urls.append(url)
  return urls

def img_name_key(img_name):
  """Used to order the urls in increasing order by 2nd word if present."""
  match = re.search(r'-(\w+)-(\w+)\.\w+', img_name)
  if match:
    return match.group(2)
  else:
    return img_name

def download_images(img_urls, dst_dir):
  """Given the urls already in the correct order, downloads
  each image into the given directory.
  Gives the images local filenames img0, img1, and so on.
  Creates an index.html in the directory
  with an img tag to show each local image file.
  Creates the directory if necessary.
  """
  if not os.path.exists(dst_dir):
    os.mkdir(dst_dir)
  
  img_names = []
  for img_url in img_urls:
    img_url_path = urllib.parse.urlsplit(img_url).path
    img_name = os.path.basename(img_url_path)
    img_file_path = os.path.join(dst_dir, img_name)
    if not os.path.exists(img_file_path):
      print("Downloading", img_url, "to:", img_file_path)
      urllib.request.urlretrieve(img_url, img_file_path)
    img_names.append(img_name)

  print(f"Found {len(img_names)} images")
  
  return sorted(list(set(img_names)), key=img_name_key)

def create_html(img_names, dst_dir):
  html_path = os.path.join(dst_dir, "index.html")
  html = open(html_path, "wt")
  html.write("<html><body>\n")
  for img_name in img_names:
    html.write(f'<img src="{img_name}">')
  html.write("</body></html>")
  html.close()

  print(f"Created {html_path} using {len(img_names)} images")


def main():
  args = sys.argv[1:]

  if not args:
    print('usage: [--todir dir] logfile ')
    sys.exit(1)

  dst_dir = os.path.join(os.getcwd(), "out")
  if args[0] == '--todir':
    dst_dir = args[1]
    del args[0:2]

  img_urls = read_urls(args[0])
  img_names = download_images(img_urls, dst_dir)
  create_html(img_names, dst_dir)

if __name__ == '__main__':
  main()
