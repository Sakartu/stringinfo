import string
import textwrap
from plugins import BasePlugin

__author__ = 'peter'


class XORPlugin(BasePlugin):
    short_description = 'XOR of the hex inputs'
    default = False
    description = textwrap.dedent('''
    This plugin XOR's all hexstrings from the input with eachother, in order.
    '''.strip())

    def sentinel(self):
        # Only parse if all inputs are valid hex strings
        try:
            for s in self.args['STRING']:
                int(s, 16)
        except ValueError:
            return False
        # Only parse if there are more than one string
        return len(self.args['STRING']) > 1

    def handle(self):
        r = int(self.args['STRING'][0], 16)
        for s in self.args['STRING'][1:]:
            r ^= int(s, 16)
        return hex(r)