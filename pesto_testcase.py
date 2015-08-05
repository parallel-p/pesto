import unittest
import configparser
import os.path

class PestoTestCase(unittest.TestCase):

    def __init__(self, *p, **d):
        super().__init__(*p, **d)
        parser = configparser.ConfigParser()
        parser.read('unittest.cfg')
        if 'dirs' in parser and 'temp_dir' in parser['dirs'] and os.path.isdir(parser['dirs']['temp_dir']):
            self.temp_dir = parser['dirs']['temp_dir'].rstrip('/').rstrip('\\') + os.path.sep
        else:
            self.temp_dir = '.' + os.path.sep
