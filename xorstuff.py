#!/usr/bin/python

import argparse
import itertools
from itertools import izip, cycle, product
from sys import exit
import shutil
import os
import string
from subprocess import Popen, PIPE

list_types = {'elf': '\x45\x6C\x66\x46\x69\x6C\x65\x00',
              'bmp': '\x42\x4d',
              'jpg': '\xFF\xD8\xFF\xE1',
              'png': '\x89\x50\x4E\x47\x0D\x0A\x1A\x0A',
              'wav': '\x52\x49\x46\x46'}


def xor(data, key):
    return ''.join(chr(ord(x) ^ ord(y)) for (x,y) in izip(data, cycle(key)))

def getFileContent(filepath, length=None):
    bin_file = ''
    with open(filepath, "rb") as f:
        byte = f.read(1)
        index = 0
        while byte != "":
            bin_file = bin_file + byte
            byte = f.read(1)
            if length is not None:
                if index == length:
                    break
                index = index + 1
    return bin_file

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='xor stuff with other stuff')
    parser.add_argument('-f', '--file', 
                        action='store', 
                        dest='filename', 
                        help='input file')
    parser.add_argument('-t', '--type',
                        action="store",
                        dest='type',
                        help='filetype',
                        choices=list_types.keys())
    parser.add_argument('-l', '--length',
                        action="store",
                        dest="key_length",
                        default=None,
                        help="key_length")
    parser.add_argument('-x', '--xor',
                        action='store',
                        dest='xor_key',
                        default=None,
                        help='xor with given key')
    args = parser.parse_args()

    # xor with one key
    if args.xor_key is not None:
        file = getFileContent(args.filename)
        xored_data = xor(file, args.xor_key)
        print xored_data
        exit(0)

    # select correct header
    header = list_types[args.type]

    # pad for bruteforce
    key_length = len(header)
    if args.key_length is not None:
            if int(args.key_length) > len(header):
                header = "%s%s" % (header, '%s' * (int(args.key_length) - len(header.replace('%s', '?'))))
            key_length = int(args.key_length)
    bf_length = header.count('%s')
    bin_file = getFileContent(args.filename, len(header.replace('%s', '?')))

    charset = ''.join([chr(i) for i in range(128)])
    key_charset = string.ascii_letters + string.digits + string.punctuation

    # generate keys
    for char in itertools.product(charset, repeat=bf_length):
        generated_header = header % char
        output = xor(bin_file,generated_header)
        key = output[0: key_length]
        if not [c for c in key if c not in key_charset]:
            print key
