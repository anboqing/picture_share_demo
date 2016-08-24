import unittest

from picture_share import app

class PictureShare(unittest.TestCase):
    def setUp(self):
        print "set up"

    def setUpClass(cls):
        print "setupclass"

    def tearDown(self):
        print "teardown"

    def test1(self):
        print "test1"

    def test2(self):
        print "test2"

    def test3(self):
        print "test3"
