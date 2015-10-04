from unittest import TestCase
from db.controller import Mongo

__author__ = 'kimothy'


class TestMongo(TestCase):

    def test_get_server(self):
        self.test_db = Mongo()
        

    def test_push(self):
        self.fail()