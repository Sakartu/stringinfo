#!/usr/bin/env python3
# -*- coding: utf8 -*-
"""
Usage:
stringinfo parse [--all] STRING...
stringinfo list


Options:
STRING          One or more strings for which you want information
--all           Run all plugins, even the ones that aren't default
"""
import colorama

from docopt import docopt
import plugins

__author__ = 'peter'


def main():
    args = docopt(__doc__)


    # Find plugins
    ps = plugins.get_plugins()

    if args['list']:
        for p in ps:
            print(p.name)
            print(p.description)
        return
    # Initialize colorama
    colorama.init()

    # For each plugin, check if it's applicable and if so, run it
    for p in ps:
        plugin = p(args)
        if (args['--all'] or plugin.default) and plugin.sentinel():
            print(plugin.short_description)
            print(plugin.handle())


if __name__ == '__main__':
    main()