from functools import reduce
import operator
import textwrap

from plugins import BasePlugin


__author__ = 'peter'


class XORPlugin(BasePlugin):
    short_description = 'XOR all hexstring input(s) with eachother'
    header = 'XOR of the hex inputs'
    default = False
    description = textwrap.dedent('''\
    This plugin XOR's all hexstrings from the input with eachother, in order.''')
    key = '--xor'

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
        ints = [int(x, 16) for x in self.args['STRING']]
        max_len = max(map(len, map(hex, ints))) - 2  # Remove 0x

        result = '\n'.join('0x{:0{ml}x}'.format(x, ml=max_len) for x in ints)

        result += '\n' + '=' * (max_len + 2) + ' ^'

        result += '\n0x{:0{ml}x}'.format(reduce(operator.xor, ints), ml=max_len)
        return result
