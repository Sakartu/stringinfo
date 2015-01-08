import textwrap
import binascii
import unicodedata

from plugins import BasePlugin


__author__ = 'peter'


class DecodeHexPlugin(BasePlugin):
    short_description = 'Decode hex string to encodings:'
    default = True
    description = textwrap.dedent('''
    This plugin tries to decode the given hexstring with the most used encodings, then print it.
    It tries to remove control characters from the string after decoding to prevent terminal breakage.
    The encodings are sorted according to their usage, see
    http://w3techs.com/technologies/overview/character_encoding/all
    '''.strip())

    def sentinel(self):
        try:
            for s in self.args['STRING']:
                binascii.unhexlify(s)
        except ValueError:
            return False
        return True

    def handle(self):
        result = ''
        for s in self.args['STRING']:
            if len(self.args['STRING']) > 1:
                result += '{0}:\n'.format(s)
            binary = binascii.unhexlify(s)

            result += self._decode('UTF8', 'utf8', binary)
            result += self._decode('iso-8859-1 (Cyrillic)', 'iso-8859-1', binary)
            result += self._decode('windows-1251 (Cyrillic)', 'cp1251', binary)
            result += self._decode('gb2312 (Chinese)', 'gb2312', binary)
            result += self._decode('Shift-JIS (Chinese)', 'shift-jis', binary)
            result += self._decode('windows-1252 (Latin)', 'cp1252', binary)
            result += self._decode('EUC-KR (Korean)', 'euc-kr', binary)
            result += self._decode('GBK (Chinese)', 'gbk', binary)

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
