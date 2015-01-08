import string
import textwrap
from plugins import BasePlugin

__author__ = 'peter'


class BasicInfoPlugin(BasePlugin):
    name = 'BasicInfoPlugin'
    short_description = 'Basic info:'
    default = True
    description = textwrap.dedent('''
    This plugin provides some basic info about the string such as:
    - Length
    - Presence of alpha/digits/raw bytes
    ''')

    def handle(self):
        result = ''
        for s in self.args['STRING']:
            if len(self.args['STRING']) > 1:
                result += '{0}:\n'.format(s)
            result += 'len: {0}\n'.format(len(s))
            result += 'number of digits: {0}\n'.format(sum(x.isdigit() for x in s))
            result += 'number of alpha: {0}\n'.format(sum(x.isalpha() for x in s))
            result += 'number of unprintable: {0}\n'.format(sum(x in string.printable for x in s))

        return result