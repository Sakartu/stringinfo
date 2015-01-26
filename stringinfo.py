#!/usr/bin/env python3
# -*- coding: utf8 -*-
"""
Usage:
stringinfo [options] [--] [STRING]...

Options:
STRING          The strings for which you want information. If none are given, read from stdin upto EOF.
--list          List all plugins, with their descriptions and whether they're default or not
--all           Run all plugins, even the ones that aren't default
--verbose       Print debugging messages
--file INFILE   Read inputs from inputfile, removing trailing newlines. BEWARE: leading/trailing whitespace is preserved!

Plugins:
"""
import colorama

from docopt import docopt
import sys
import veryprettytable
import plugins
from plugins.util import color

__author__ = 'peter'


def main():
    args = docopt(__doc__ + plugins.usage_table())

    # Find plugins
    ps = plugins.get_plugins(args)

    if args['--list']:
        table = veryprettytable.VeryPrettyTable()
        table.field_names = ('Name', 'Default', 'Description')
        table.align = 'l'
        for p in ps:
            table.add_row((p.__name__,
                           color(p.default),
                           p.description))
        print(table)
        return

    if args['--file']:
        args['STRING'] = [x.strip('\n\r') for x in open(args['--file'], 'r')]

    if not args['STRING']:
        args['STRING'] = [sys.stdin.read()]

    # Initialize colorama
    colorama.init()

    # For each plugin, check if it's applicable and if so, run it
    for p in ps:
        plugin = p(args)
        if plugin.sentinel():
            print(plugin.header)
            print(plugin.handle())
        else:
            if args['--verbose']:
                print('Sentinel failed for {0}'.format(p.__name__))


if __name__ == '__main__':
    main()