#!/usr/bin/env python3
# -*- coding: utf8 -*-
"""
Usage:
stringinfo.py STRING
STRING          The string of which you want information
"""

from docopt import docopt
import plugins

__author__ = 'peter'


def main():
    args = docopt(__doc__)
    print(args)

    # Find plugins
    p = plugins.get_plugins()
    # For each plugin, check if it's applicable and if so, run it


if __name__ == '__main__':
    main()