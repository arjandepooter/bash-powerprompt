#!/usr/bin/env python
# -*- coding: utf-8 -*-
from powerprompt.core import PowerPrompt
import json
import os
import sys

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--conf-file",
                        help="the configuration file to use",
                        default=open(os.path.join(os.environ.get('HOME'),
                                             '.powerprompt' ,'config.json')),
                        type=argparse.FileType('r'))
    parser.add_argument("return_code",
                        help="exit code of last command",
                        nargs="?",
                        default=0,
                        type=int)
    args = parser.parse_args()

    try:
        settings = json.load(args.conf_file)
    except:
        settings = {}

    prompt = PowerPrompt(settings)
    sys.stdout.write('%s' % (prompt.render()))

if __name__ == '__main__':
    main()