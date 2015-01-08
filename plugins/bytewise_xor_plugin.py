import textwrap
import binascii

from plugins import BasePlugin


__author__ = 'peter'


class BytewiseXORPlugin(BasePlugin):
    short_description = 'XOR of each byte of the hex inputs:'
    default = False
    description = textwrap.dedent('''\
    This plugin XOR's all hexstrings from the input with eachother, in order. It sees each string as a list of hex
    encoded bytes, so 0140b6 (hex) will be seen as 01, 64 and 182 (decimal). Hexstrings will be prepended with zeroes
    if they are not of equal length.''')

    def sentinel(self):
        # Only parse if all inputs are valid hex strings
        try:
            for s in self.args['STRING']:
                binascii.unhexlify(s)
        except ValueError:
            return False
        # Only parse if there are more than one string
        return len(self.args['STRING']) > 1

    def handle(self):
        inputs = self._prepend_zeroes(self.args['STRING'])
        r = binascii.unhexlify(inputs[0])
        for s in inputs[1:]:
            s = binascii.unhexlify(s)
            r = ''.join('{0:0>2x}'.format(c1 ^ c2) for c1, c2 in zip(r, s))
        return r

    @staticmethod
    def _prepend_zeroes(params):
        maxlen = max(map(len, params))
        return [x.rjust(maxlen, '0') for x in params]
