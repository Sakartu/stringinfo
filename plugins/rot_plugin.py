import string
import textwrap

from veryprettytable import VeryPrettyTable

from plugins import BasePlugin


__author__ = 'peter'


class RotPlugin(BasePlugin):
    short_description = 'Produce all possible ROT(n) versions of the input(s)'
    header = 'Rot(n) versions of strings'
    default = True
    description = textwrap.dedent('''\
    This plugin produces all possible Rot(n) versions of the given string.''')
    key = '--rot'

    def handle(self):
        result = ''
        for s in self.args['STRING']:
            if len(self.args['STRING']) > 1:
                result += '{0}:\n'.format(repr(s))
            for i in range(26):
                result += 'ROT{0:02d}: {1}\n'.format(i, self._rot(s, i))
        return result

    @staticmethod
    def _rot(s, n):
        lc = string.ascii_lowercase
        uc = string.ascii_uppercase
        lookup = str.maketrans(lc + uc, lc[n:] + lc[:n] + uc[n:] + uc[:n])
        return s.translate(lookup)

