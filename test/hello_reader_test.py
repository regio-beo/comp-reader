import unittest

from compreader.hello_reader import HelloReader

class HelloReaderTest(unittest.TestCase):

    def test_read(self):
        reader = HelloReader()
        self.assertEqual("hello", reader.read())
        
