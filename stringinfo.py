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

Plugins:
"""
# --basic         Run the basic info plugin
# --hash          Run the hash plugin
# --xor           Run the XOR plugin
# --bytewise-xor  Run the bytewise XOR plugin
# --decode-hex    Run the decode-hex plugin
# --alphabet      Run the alphabet plugin
# --rot           Run the ROT(n) plugin
# """
import colorama

from docopt import docopt
from colorama import Fore
import sys
import veryprettytable
import plugins

__author__ = 'peter'


def main():
    d = __doc__
    d += plugins.usage_table()
    args = docopt(d)

    # Find plugins
    ps = plugins.get_plugins(args)

    if args['--list']:
        table = veryprettytable.VeryPrettyTable()
        table.field_names = ('Name', 'Default', 'Description')
        table.align = 'l'
        for p in ps:
            table.add_row((p.__name__,
                           Fore.GREEN + '✔' + Fore.RESET if p.default else Fore.RED + '✗' + Fore.RESET,
                           p.description))
        print(table)
        return

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