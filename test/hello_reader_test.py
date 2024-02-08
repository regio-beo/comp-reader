import unittest

from compreader.hello_reader import CompetitionFile

class HelloReaderTest(unittest.TestCase):

    def test_read(self):
        reader = CompetitionFile()
        self.assertEqual("hello", reader.read())
        
