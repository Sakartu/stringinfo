import string
import textwrap
import binascii
import unicodedata
from veryprettytable import VeryPrettyTable
from plugins import BasePlugin

__author__ = 'peter'


class DecodeHexPlugin(BasePlugin):
    short_description = 'Decode hex string to encodings:'
    default = True
    description = textwrap.dedent('''
    This plugin tries to decode the given hexstring with some common encodings, then print it.
    It tries to remove control characters from the string after decoding to prevent terminal breakage.
    '''.strip())

    def sentinel(self):
        return all(not len(x) % 2 for x in self.args['STRING'])

    def handle(self):
        result = ''
        for s in self.args['STRING']:
            if len(self.args['STRING']) > 1:
                result += '{0}:\n'.format(s)
            binary = binascii.unhexlify(s)

            result += self._decode('UTF8', 'utf8', binary)
            result += self._decode('iso-8859-1 (Cyrillic)', 'iso-8859-1', binary)

        return result

    def _decode(self, name, encoding, binary):
        try:
            s = self._clean(binary.decode(encoding))
        except UnicodeDecodeError:
            s = '<invalid>'
        return '{0}: "{1}"\n'.format(name, s)

    @staticmethod
    def _clean(s):
        return "".join(ch for ch in s if unicodedata.category(ch)[0] != "C")
