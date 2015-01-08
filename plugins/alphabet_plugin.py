import string
import textwrap
import binascii

from veryprettytable import VeryPrettyTable

from plugins import BasePlugin


__author__ = 'peter'


class AlphabetPlugin(BasePlugin):
    short_description = 'As index in the alphabet:'
    default = True
    description = textwrap.dedent('''\
    This plugin only works when (at least one of the) string(s) is either a concatenation of decimals, or a hex string.
    This plugin will try to use character pairs from the string as indexes in the alphabet, such that 01 is 'a',
    02 is 'b', etc. If the string is a hexstring the pairs will first be converted to integers.''')

    def sentinel(self):
        for s in self.args['STRING']:
            if all(x.isdigit() for x in s):
                # All digits
                if all(0 <= int(x) <= 26 for x in self._chunks(s, 2)):
                    # All between 0 and 26
                    return True

            try:
                if all(0 <= int(x) <= 26 for x in binascii.unhexlify(s)):
                    return True
            except ValueError:
                continue
        return False

    def handle(self):
        result = ''
        for s in self.args['STRING']:
            if len(self.args['STRING']) > 1:
                result += '{0}:\n'.format(s)
            try:
                result += 'As decimals: {0}\n'.format(''.join(string.ascii_lowercase[int(x)] for x in self._chunks(s, 2)))
            except ValueError:
                pass

            try:
                indexes = [x for x in binascii.unhexlify(s)]
                result += 'As hex: {0}\n'.format(''.join(string.ascii_letters[x] for x in indexes))
            except ValueError as e:
                print(e)
        return result

    @staticmethod
    def _chunks(s, n):
        for i in range(0, len(s), n):
            yield s[i:i+n]