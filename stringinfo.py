#!/usr/bin/env python3
# -*- coding: utf8 -*-
"""
Usage:
stringinfo STRING...

Options:
STRING          One or more strings for which you want information
"""
import colorama

from docopt import docopt
import plugins

__author__ = 'peter'


def main():
    args = docopt(__doc__)

    # Find plugins
    ps = plugins.get_plugins()

    # Initialize colorama
    colorama.init(autoreset=True)

    # For each plugin, check if it's applicable and if so, run it
    for p in ps:
        plugin = p(args)
        if plugin.sentinel():
            print(plugin.short_description)
            print(plugin.handle())


if __name__ == '__main__':
    main()