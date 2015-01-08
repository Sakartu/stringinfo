import string
import textwrap
from colorama import Fore, Style
from veryprettytable import VeryPrettyTable
from plugins import BasePlugin

__author__ = 'peter'

# From: http://en.wikipedia.org/wiki/List_of_hash_functions
CRC = [
    ('BSD checksum', 16, lambda x: len(x) == 4),
    ('checksum', 32, lambda x: len(x) == 8),
    ('crc16', 16, lambda x: len(x) == 4),
    ('crc32', 32, lambda x: len(x) == 8),
    ('crc32 mpeg2', 32, lambda x: len(x) == 8),
    ('crc64', 64, lambda x: len(x) == 16),
    ('SYSV checksum', 16, lambda x: len(x) == 4),
]

CHECKSUMS = [
    ('sum (Unix)', '16 or 32', lambda x: len(x) in (4, 8)),
    ('sum8', 8, lambda x: len(x) == 2),
    ('sum16', 16, lambda x: len(x) == 4),
    ('sum24', 24, lambda x: len(x) == 6),
    ('sum32', 32, lambda x: len(x) == 8),
    ('fletcher-4', 4, lambda x: len(x) == 1),
    ('fletcher-8', 8, lambda x: len(x) == 2),
    ('fletcher-16', 16, lambda x: len(x) == 4),
    ('fletcher-32', 32, lambda x: len(x) == 8),
    ('Adler-32', 32, lambda x: len(x) == 8),
    ('xor8', 8, lambda x: len(x) == 2),
    ('Luhn algorithm', 4, lambda x: len(x) == 1),
    ('Verhoeff algorithm', 4, lambda x: len(x) == 1),
    ('Damm algorithm', '1 decimal digit', lambda x: len(x) == 1 and x.isdigit()),
]

NON_CRYPTO_HASHES = [
    ('Pearson hashing', 8, lambda x: len(x) == 2),
    ('Buzhash', 'variable', lambda x: True),  # variable length
    ('Fowler–Noll–Vo hash function (FNV Hash)', '32, 64, 128, 256, 512 or 1024', lambda x: len(x) in (8, 16, 32, 64, 128, 256)),
    ('Zobrist hashing', 'variable', lambda x: True),
    ('Jenkins hash function', '32 or 64', lambda x: len(x) in (8, 16)),
    ('Java hashCode()', 32, lambda x: len(x) == 8),
    ('Bernstein hash', 32, lambda x: len(x) == 8),
    ('elf64', 64, lambda x: len(x) == 16),
    ('MurmurHash', '32, 64 or 128', lambda x: len(x) in (8, 16, 32)),
    ('SpookyHash', '32, 64 or 128', lambda x: len(x) in (8, 16, 32)),
    ('CityHash', '64, 128 or 256', lambda x: len(x) in (16, 32, 64)),
    ('numeric hash (nhash)', 'variable', lambda x: True),
    ('xxHash', '32 or 64', lambda x: len(x) in (8, 16)),
]

CRYPTO_HASHES = [
    ('BLAKE-256', 256, lambda x: len(x) == 64),
    ('BLAKE-512', 512, lambda x: len(x) == 128),
    ('ECOH', '224 to 512', lambda x: 56 >= len(x) >= 128),
    ('FSB', '160 to 512', lambda x: 40 >= len(x) >= 128),
    ('GOST', 256, lambda x: len(x) == 64),
    ('Grøstl', '256 to 512', lambda x: 64 >= len(x) >= 128),
    ('HAS-160', 160, lambda x: len(x) == 40),
    ('HAVAL', '128 to 256', lambda x: 32 >= len(x) >= 64),
    ('JH', 512, lambda x: len(x) == 128),
    ('MD2', 128, lambda x: len(x) == 32),
    ('MD4', 128, lambda x: len(x) == 32),
    ('MD5', 128, lambda x: len(x) == 32),
    ('MD6', 512, lambda x: len(x) == 128),
    ('RadioGatún', 'upto 1216', lambda x: len(x) <= 304),
    ('RIPEMD', 128, lambda x: len(x) == 32),
    ('RIPEMD-128', 128, lambda x: len(x) == 32),
    ('RIPEMD-160', 160, lambda x: len(x) == 40),
    ('RIPEMD-320', 320, lambda x: len(x) == 80),
    ('SHA-1', 160, lambda x: len(x) == 40),
    ('SHA-224', 224, lambda x: len(x) == 56),
    ('SHA-256', 256, lambda x: len(x) == 64),
    ('SHA-384', 384, lambda x: len(x) == 96),
    ('SHA-512', 512, lambda x: len(x) == 128),
    ('SHA-3 (originally known as Keccak)', 'arbitrary', lambda x: True),
    ('Skein', 'arbitrary', lambda x: True),
    ('SipHash', 64, lambda x: len(x) == 16),
    ('Snefru', '128 or 256', lambda x: len(x) in (32, 64)),
    ('Spectral Hash', 512, lambda x: len(x) == 128),
    ('SWIFFT', 512, lambda x: len(x) == 128),
    ('Tiger', 192, lambda x: len(x) == 48),
    ('Whirlpool', 512, lambda x: len(x) == 128),
]


class HashPlugin(BasePlugin):
    short_description = 'Hashes:'
    default = True
    description = textwrap.dedent('''
    This plugin tries to see if the provided string could possibly be a hash in hex notation of some kind
    '''.strip())

    def handle(self):
        result = ''
        for s in self.args['STRING']:
            if len(self.args['STRING']) > 1:
                result += '{0}:\n'.format(s)

            result += self._print_table('Cyclic Redundancy Checks:', s, CRC)
            result += self._print_table('Checksums:', s, CHECKSUMS)
            result += self._print_table('Non-cryptographic hash functions:', s, NON_CRYPTO_HASHES)
            result += self._print_table('Cryptographic hash functions:', s, CRYPTO_HASHES)
        return result

    def _print_table(self, name, s, to_check):
        result = name + '\n'
        table = VeryPrettyTable()
        table.field_names = ('name', 'length (bits)', 'viable?')
        table.align['name'] = 'l'

        for x in self._check_table(s, to_check):
            table.add_row(x)
        result += str(table) + '\n'
        return result


    @staticmethod
    def _check_table(s, table):
        result = []
        for name, length, f in table:
            if f(s):
                result.append((name, length, Fore.GREEN + '✔' + Fore.RESET))
            else:
                result.append((name, length, Fore.RED + '✗' + Fore.RESET))
        return result

