#!/usr/bin/env python3
# -*- coding: utf8 -*-
"""
Usage:
stringinfo [--list] [--all] [--] [STRING...]


Options:
STRING          One or more strings for which you want information
--all           Run all plugins, even the ones that aren't default
--list          List all plugins, with their descriptions and whether they're default or not
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
    ps = plugins.get_plugins()

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
        if (args['--all'] or plugin.default) and plugin.sentinel():
            print(plugin.short_description)
            print(plugin.handle())


if __name__ == '__main__':
    main()