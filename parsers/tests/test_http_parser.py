from unittest import TestCase
from parsers.http_parser import *

__author__ = 'kimothy'


class TestHttpParser(TestCase):
    def test_parse_url(self):
        testList = parse_url("//foo/bar//")

        self.assertEqual(testList[0], "foo")
        self.assertEqual(testList[1], "bar")
        self.assertEqual(len(testList), 2)


    def test_parse_body(self):
        jsonExample = '{\
               "error": {\
                  "message": "(#803) Cannot query users by their username (kimothykr)",\
                  "type": "OAuthException",\
                  "code": 803,\
                  "fbtrace_id": "DtEEUjyuC6h"\
               }\
            }'

        with self.assertRaises(Exception) :
            testDictionary = parse_body('{error:te')

        testDictionary = parse_body(jsonExample)
        self.assertEqual(testDictionary["error"]["code"], 803)
        self.assertEqual(testDictionary["error"]["fbtrace_id"], "DtEEUjyuC6h")
        self.assertEqual(len(testDictionary), 1)
        self.assertEqual(len(testDictionary["error"]), 4)

