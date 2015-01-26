from colorama import Fore

__author__ = 'peter'


def green(s):
    return Fore.GREEN + s + Fore.RESET


def red(s):
    return Fore.RED + s + Fore.RESET


def yellow(s):
    return Fore.YELLOW + s + Fore.RESET


def color(test, t='✔', f='✗', n='?'):
    if test is None:
        return yellow(n)
    elif test:
        return green(t)
    else:
        return red(f)
