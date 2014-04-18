#!/usr/bin/python

import argparse
import itertools
from itertools import izip, cycle, product
from sys import exit
import shutil
import os
import string
from subprocess import Popen, PIPE
import glob
from moduleBaseClass import ModuleBaseClass
from guess_keylength import GuessKeyLength
from operator import itemgetter

list_types = {}

def loadFilesTypes(path):
    list_types = {}
    files = glob.glob(path + "*")
    for file in files:
        file_name, file_extension = os.path.splitext(file)
        if not file_name.endswith("__init__") and file_extension == ".py":
            module_name = file_name.replace("/", ".")
            mod = __import__(module_name)
            modules = module_name.split('.')
            for module in modules[1:]:
                mod = getattr(mod, module)
                if issubclass(mod.Module, ModuleBaseClass):
                    instance = mod.Module()
                    list_types[instance.name] = instance
    return list_types

def xor(data, key, file_type=None):
    result = []
    for data, char_key in izip(data, cycle(key)):
        byte = chr(ord(data) ^ ord(char_key))
        if file_type is not None:
            if not file_type.live_check(byte):
                return None
        result.append(byte)
    return ''.join(result)

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

    # Load modules
    list_types = loadFilesTypes('modules/')

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
    parser.add_argument('-g', '--grep',
                        action='store_true',
                        dest='grep',
                        default=None,
                        help='Search pattern in result')
    args = parser.parse_args()

    # xor with one key
    if args.xor_key is not None:
        file = getFileContent(args.filename)
        xored_data = xor(file, args.xor_key)
        print xored_data
        exit(0)
    elif args.type is None or args.filename is None:
        print "Select file type (-t) and filename (-f)"
        exit(0)

    print "[*] Open file"
    bin_file = getFileContent(args.filename)
    file_type = list_types[args.type]
    # select correct header
    header = file_type.header

    # pad for bruteforce
    key_length = len(header)
    if args.key_length is not None:
            key_length = int(args.key_length)
    else:
        guess = GuessKeyLength()
        print "[*] Guess key length"
        key_length = guess.guess_key_length(bin_file)
        fitnesses = guess.print_fitnesses()
        divisors = guess.guess_and_print_divisors()
        print "[*] Probable key length"
        fitnesses = sorted(fitnesses, key=lambda fitness: float(fitness['percents']), reverse=True) 
        for fitness in fitnesses:
            print "    %s : %s%%" % (fitness['length'], fitness['percents'])
        print "[*] Most probable key length is %s*n" % divisors

    for fitness in fitnesses:
        key_length = int(fitness['length'])
        print "[*] Key length set to %d" % key_length

        # Padding of header with %s if key length > header length
        if int(key_length) > len(header):
            header = "%s%s" % (header, '%s' * (int(key_length) - len(header.replace('%s', '?'))))

        bf_length = header.count('%s')
        bin_header = getFileContent(args.filename, len(header.replace('%s', '?')))

        charset = ''.join([chr(i) for i in range(128)])
        key_charset = string.ascii_letters + string.digits + string.punctuation

        # generate keys
        for char in itertools.product(charset, repeat=bf_length):
            generated_header = header % char
            output = xor(bin_header, generated_header)
            key = output[0: key_length]
            if not [c for c in key if c not in key_charset]:
                raw = xor(bin_file, key, file_type)
                if raw is not None:
                    if file_type.final_check(raw):
                        if args.grep is not None:
                            if args.grep in raw:
                                print key
                        else:
                            print key
