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

class XorStuff:

    def __init__(self, list_types={}):
        self.list_types = list_types
        self.file_type = None

    def loadFilesTypes(self, path):
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

    def xor(self, data, key, file_type=None):
        result = []
        for data, char_key in izip(data, cycle(key)):
            byte = chr(ord(data) ^ ord(char_key))
            if file_type is not None:
                if not file_type.live_check(byte):
                    return None
            result.append(byte)
        return ''.join(result)

    def getFileContent(self, filepath, length=None):
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

    def get_pass(self, bin_file, key_length, grep=None):
        header = self.file_type.header
        # Padding of header with %s if key length > header length
        if int(key_length) > len(header):
            header = "%s%s" % (header, '%s' * (int(key_length) - len(header.replace('%s', '?'))))

        bf_length = header.count('%s')
        bin_header = self.getFileContent(args.filename, len(header.replace('%s', '?')))

        charset = ''.join([chr(i) for i in range(128)])
        key_charset = string.ascii_letters + string.digits + string.punctuation

        # generate keys
        for char in itertools.product(charset, repeat=bf_length):
            generated_header = header % char
            output = self.xor(bin_header, generated_header)
            key = output[0: key_length]
            if not [c for c in key if c not in key_charset]:
                raw = self.xor(bin_file, key, self.file_type)
                if raw is not None:
                    if self.file_type.final_check(raw):
                        if grep is not None:
                            if grep in raw:
                                yield key
                        else:
                            yield key

    def set_file_type(self, file_type):
        self.file_type = self.list_types[file_type]

if __name__ == "__main__":

    # Load modules
    xor_stuff = XorStuff()
    xor_stuff.list_types = xor_stuff.loadFilesTypes('modules/')

    parser = argparse.ArgumentParser(description='xor stuff with other stuff')
    parser.add_argument('-f', '--file', 
                        action='store', 
                        dest='filename', 
                        help='input file')
    parser.add_argument('-t', '--type',
                        action="store",
                        dest='type',
                        help='filetype',
                        choices=xor_stuff.list_types.keys())
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
        file = xorstuff.getFileContent(args.filename)
        print  xor_stuff.xor(file, args.xor_key)
        exit(0)
    elif args.type is None or args.filename is None:
        print "Select file type (-t) and filename (-f)"
        exit(0)

    # Open input file
    print "[*] Open file"
    bin_file = xor_stuff.getFileContent(args.filename)
    xor_stuff.set_file_type(args.type)

    # Search key length
    key_length = len(xor_stuff.file_type.header)
    if args.key_length is not None:
            key_length = int(args.key_length)
            fitnesses = [{'length': key_length, 'percents': 100}]
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

    # Search password
    for fitness in fitnesses:
        key_length = int(fitness['length'])
        print "[*] Key length set to %d" % key_length

        for password in xor_stuff.get_pass(bin_file, key_length, args.grep):
            print password
