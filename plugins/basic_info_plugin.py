import string
import textwrap

from veryprettytable import VeryPrettyTable

from plugins import BasePlugin


__author__ = 'peter'


class BasicInfoPlugin(BasePlugin):
    short_description = 'Basic info:'
    default = True
    description = textwrap.dedent('''\
    This plugin provides some basic info about the string such as:
    - Length
    - Presence of alpha/digits/raw bytes''')

    def handle(self):
        table = VeryPrettyTable()
        table.field_names = ['String', 'Length', '# Digits', '# Alpha', '# Punct.', '# Control']
        for s in self.args['STRING']:
            table.add_row((s, len(s), sum(x.isdigit() for x in s), sum(x.isalpha() for x in s),
                           sum(x in string.punctuation for x in s), sum(x not in string.printable for x in s)))

        return str(table) + '\n'