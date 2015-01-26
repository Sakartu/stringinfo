import string
import textwrap

from veryprettytable import VeryPrettyTable

from plugins import BasePlugin, color


__author__ = 'peter'


class AlphabetPlugin(BasePlugin):
    short_description = 'Show the alphabet of the given input(s)'
    header = 'Alphabet:'
    default = True
    description = textwrap.dedent('''\
    This plugin shows the alphabet of the given input, including which characters are missing''')
    key = '--alphabet'

    def handle(self):
        alphabet = string.printable.strip()
        table = VeryPrettyTable()
        table.field_names = ['String', 'Alphabet']
        for s in self.args['STRING']:
            result = ''.join(color(x in s, x, x) for x in alphabet)
            table.add_row((repr(s), result))

        return str(table) + '\n'