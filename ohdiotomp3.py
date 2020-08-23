#!/usr/bin/python3

import argparse
import os
import sys

if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")

def run_command(cmd):
    status = os.system(cmd)
    if(status != 0):
        print("Command %s return status %d" % (cmd, status))
        sys.exit(1)

def fetch_mp4(path):
    mp4list = []
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            fullpath = os.path.join(root,name)
            filename, ext = os.path.splitext(fullpath)
            if not "mp4" in ext.lower():
                continue

            mp4list.append(fullpath.replace("./",""))

    return mp4list

def transcode_mp4list(mp4list):
    for input_file in mp4list:
        output_file = input_file.replace("mp4","mp3")

        if os.path.exists(output_file):
            print("Skipping existing %s" % (output_file))
            continue

        cmd = "ffmpeg -i %s %s" % (input_file, output_file)
        print("Executing: %s" % (cmd))
        run_command(cmd)

parser = argparse.ArgumentParser(description="ohdiotomp3.py convert mp4 to mp3")
parser.add_argument("--sourcedir", type=str, default=".", help="directory where your mp4 are found")
args = parser.parse_args()

mp4list = fetch_mp4(args.sourcedir)
transcode_mp4list(mp4list)