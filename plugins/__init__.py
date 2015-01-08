import os

__author__ = 'peter'


def get_plugins():
    result = []
    for name in os.listdir(os.path.dirname(__file__)):
        if not name.endswith('_plugin.py'):
            continue
        name = 'plugins.' + name[:-3]
        i = __import__(name, fromlist=[''])
        for c in dir(i):
            if c.endswith('Plugin') and c != 'BasePlugin':
                result.append(getattr(i, c))
    return result


class BasePlugin():
    def __init__(self, args):
        self.args = args

    def sentinel(self):
        """
        A method which should be called to test if this plugin is viable for the given input
        :return: True if this plugin is viable for the given input
        """
        return True

    def handle(self):
        """
        The method which does the actual work.
        :return: A string forming the output of this plugin.
        """
        raise NotImplementedError
