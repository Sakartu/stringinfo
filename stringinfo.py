#!/usr/bin/env python3
# -*- coding: utf8 -*-
"""
Usage:
stringinfo [--list] [--all] [--basic] [--hash] [--xor] [--bytewise-xor] [--decode-hex] [--alphabet] [--rot] [--verbose] [--] [STRING...]

Options:
STRING          One or more strings for which you want information
--all           Run all plugins, even the ones that aren't default
--list          List all plugins, with their descriptions and whether they're default or not
--basic         Run the basic info plugin
--hash          Run the hash plugin
--xor           Run the XOR plugin
--bytewise-xor  Run the bytewise XOR plugin
--decode-hex    Run the decode-hex plugin
--alphabet      Run the alphabet plugin
--rot           Run the ROT(n) plugin
--verbose       Print debugging messages
"""
import colorama

from docopt import docopt
from colorama import Fore
from veryprettytable import VeryPrettyTable
import plugins

__author__ = 'peter'


def main():
    args = docopt(__doc__)

    # Find plugins
    ps = plugins.get_plugins(args)

    if args['--list']:
        table = VeryPrettyTable()
        table.field_names = ('Name', 'Default', 'Description')
        table.align = 'l'
        for p in ps:
            table.add_row((p.__name__,
                           Fore.GREEN + '✔' + Fore.RESET if p.default else Fore.RED + '✗' + Fore.RESET,
                           p.description))
        print(table)
        return
    # Initialize colorama
    colorama.init()

    # For each plugin, check if it's applicable and if so, run it
    for p in ps:
        plugin = p(args)
        if plugin.sentinel():
            print(plugin.short_description)
            print(plugin.handle())
        else:
            if args['--verbose']:
                print('Sentinel failed for {0}'.format(p.__name__))


if __name__ == '__main__':
    main()