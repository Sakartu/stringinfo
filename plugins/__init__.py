from collections import OrderedDict
import os
import veryprettytable

__author__ = 'peter'


def all_plugins():
    result = OrderedDict()
    for name in os.listdir(os.path.dirname(__file__)):
        if not name.endswith('_plugin.py'):
            continue
        name = 'plugins.' + name[:-3]
        i = __import__(name, fromlist=[''])
        for c in dir(i):
            if c.endswith('Plugin') and c != 'BasePlugin':
                p = getattr(i, c)
                result[p.__name__] = p
    return result


def usage_table():
    t = veryprettytable.VeryPrettyTable()
    for p in all_plugins().values():
        t.add_row((p.key, p.short_description))
    t.border = False
    t.header = False
    t.align = 'l'
    return t.get_string()


def get_plugins(args):
    result = all_plugins()
    to_run = []
    if args['--all'] or args['--list']:
        to_run = result.values()
    else:
        if args['--basic']:
            to_run.append(result['BasicInfoPlugin'])
        if args['--hash']:
            to_run.append(result['HashPlugin'])
        if args['--xor']:
            to_run.append(result['XORPlugin'])
        if args['--alphabet']:
            to_run.append(result['AlphabetPlugin'])
        if args['--rot']:
            to_run.append(result['RotPlugin'])
        if args['--decode-hex']:
            to_run.append(result['DecodeHexPlugin'])
    if not to_run:
        to_run = [x for x in result.values() if x.default]

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
