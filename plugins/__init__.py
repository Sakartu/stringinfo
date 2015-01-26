import os
from colorama import Fore
import veryprettytable

__author__ = 'peter'


def all_plugins():
    result = []
    for name in os.listdir(os.path.dirname(__file__)):
        if not name.endswith('_plugin.py'):
            continue
        name = 'plugins.' + name[:-3]
        i = __import__(name, fromlist=[''])
        for c in dir(i):
            if c.endswith('Plugin') and c != 'BasePlugin':
                p = getattr(i, c)
                result.append(p)
    return result


def usage_table():
    t = veryprettytable.VeryPrettyTable()
    for p in all_plugins():
        t.add_row((p.key, p.short_description))
    t.border = False
    t.header = False
    t.align = 'l'
    return t.get_string()


def get_plugins(args):
    result = all_plugins()

    if args['--all'] or args['--list']:
        return result

    to_run = [p for p in result if args[p.key]] or [x for x in result if x.default]

    return to_run


class BasePlugin():
    def __init__(self, args):
        self.args = args

    def sentinel(self):
        """
        A method which should be called to test if this plugin is viable for the given input
        :return: True if this plugin is viable for the given input
        """
        return True

    def handle(self):
        """
        The method which does the actual work.
        :return: A string forming the output of this plugin.
        """
        raise NotImplementedError


def color(test, t='✔', f='✗', n='?'):
    if test is None:
        return yellow(n)
    elif test:
        return green(t)
    else:
        return red(f)


def yellow(s):
    return Fore.YELLOW + s + Fore.RESET


def red(s):
    return Fore.RED + s + Fore.RESET


def green(s):
    return Fore.GREEN + s + Fore.RESET