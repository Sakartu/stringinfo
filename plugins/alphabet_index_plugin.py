import string
import textwrap
import binascii

from veryprettytable import VeryPrettyTable

from plugins import BasePlugin


__author__ = 'peter'


class AlphabetIndexPlugin(BasePlugin):
    short_description = 'Use the (hex or digit) input(s) as index in the alphabet'
    header = 'As index in the alphabet:'
    default = False
    description = textwrap.dedent('''\
    This plugin only works when (at least one of the) string(s) is either a concatenation of decimals, or a hex string.
    This plugin will try to use character pairs from the string as indexes in the alphabet, such that 01 is 'a',
    02 is 'b', etc. If the string is a hexstring the pairs will first be converted to integers. The index will be used
    modulo te length of the alphabet.''')
    key = '--alphabet-index'

    def sentinel(self):
        for s in self.args['STRING']:
            try:
                map(int, s)
                return True
            except ValueError:
                pass

            try:
                map(int, binascii.unhexlify(s))
                return True
            except ValueError:
                continue
        return False

    def handle(self):
        t = VeryPrettyTable(field_names=('String', 'Method', 'Base', 'Output'))
        for s in self.args['STRING']:
            alphabet = string.ascii_lowercase

            try:
                t.add_row((repr(s), 'dec', '0-based', ''.join(alphabet[int(x) % len(alphabet)] for x in self._chunks(s, 2))))
                t.add_row((repr(s), 'dec', '1-based', ''.join(alphabet[(int(x) - 1) % len(alphabet)] for x in self._chunks(s, 2))))
            except ValueError:
                pass

            try:
                indexes = [int(x) for x in binascii.unhexlify(s)]
                t.add_row((repr(s), 'hex', '0-based', ''.join(alphabet[int(x) % len(alphabet)] for x in indexes)))
                t.add_row((repr(s), 'hex', '1-based', ''.join(alphabet[(int(x) - 1) % len(alphabet)] for x in indexes)))
            except ValueError as e:
                if self.args['--verbose']:
                    print(e)

        t.align = 'l'
        return t.get_string()

    @staticmethod
    def _chunks(s, n):
        for i in range(0, len(s), n):
            yield s[i:i+n]