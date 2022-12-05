#!/usr/bin/env python
# -*- coding: utf-8 -*-
''' A tiny random password generator '''

from os import urandom
from string import ascii_lowercase, ascii_uppercase
from argparse import ArgumentParser

def pwgen(seed):
    while True:
        yield seed[ord(urandom(1)) % len(seed)]

def main():
    default_seed = ascii_lowercase + ascii_uppercase + \
                   ''.join([str(x) for x in range(0, 10)]) + '+/'
    
    parser = ArgumentParser()
    parser.add_argument('-l', type=int, help='The length of the password to generate. '
                        'The default length is 24 characters.',
                        default=24)
    parser.add_argument('-s', type=str, help='The string of characters to use as a seed. '
                        'The default is A-Z, a-z, 0-9, and +/',
                        default=default_seed)

    args = parser.parse_args()

    pw = ''
    for a in pwgen(args.s):
        pw += a
        if len(pw) >= args.l:
            break

    print(pw.strip())


if __name__ == '__main__':
    main()
