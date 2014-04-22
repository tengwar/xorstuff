#!/usr/bin/python

import argparse
from xorstuff import XorStuff
from guess_keylength import GuessKeyLength
from sys import exit

if __name__ == "__main__":

    xor_stuff = XorStuff()

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
        xor_stuff.set_file_content(args.filename)
        xor_stuff.xor(args.xor_key)
        exit(0)
    elif args.type is None or args.filename is None:
        print "Select file type (-t) and filename (-f)"
        exit(0)

    # Open input file
    print "[*] Open file"
    xor_stuff.set_file_content(args.filename)
    xor_stuff.set_file_type(args.type)

    # Set key length
    key_length = len(xor_stuff.file_type.header)
    if args.key_length is not None:
            key_length = int(args.key_length)
            fitnesses = [{'length': key_length, 'percents': 100}]
    else:
        # Guess key length using GuessKeyLength class
        guess = GuessKeyLength()
        print "[*] Guess key length"
        key_length = guess.guess_key_length(xor_stuff.file_content)
        fitnesses = guess.print_fitnesses()
        divisors = guess.guess_and_print_divisors()
        print "[*] Probable key length"
        fitnesses = sorted(fitnesses,
                           key=lambda fitness: float(fitness['percents']),
                           reverse=True)
        for fitness in fitnesses:
            print "    %s : %s%%" % (fitness['length'], fitness['percents'])
        print "[*] Most probable key length is %s*n" % divisors

    # Search password
    for fitness in fitnesses:
        key_length = int(fitness['length'])
        print "[*] Key length set to %d" % key_length
        print "[*] Start searching password"
        for password in xor_stuff.get_pass(key_length, args.grep):
            print password
