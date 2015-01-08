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
        result = ''
        for s in self.args['STRING']:
            if len(self.args['STRING']) > 1:
                result += '{0}:\n'.format(s)
            table = VeryPrettyTable()
            table.field_names = ['Length', '# Digits', '# Alpha', '# Punct.', '# Control']
            table.add_row((len(s), sum(x.isdigit() for x in s), sum(x.isalpha() for x in s),
                           sum(x in string.punctuation for x in s), sum(x not in string.printable for x in s)))
            result += str(table) + '\n'

        return result