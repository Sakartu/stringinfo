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
        max_len = max(map(len, self.args['STRING']))
        result = '\n'.join('0x' + hex(int(x, 16))[2:].rjust(max_len - 2, '0') for x in self.args['STRING'])
        result += '\n' + '=' * max_len + ' ^'

        r = int(self.args['STRING'][0], 16)
        for s in self.args['STRING'][1:]:
            r ^= int(s, 16)
        result += '\n' + hex(r)
        return result
