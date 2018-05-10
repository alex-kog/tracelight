from unittest import TestCase

from query_routes_parser import QueryRoutesParser


class QueryRoutesParserTest(TestCase):
    def test_negative_discr(self):
        s = QueryRoutesParser()

        # self.assertRaises(Exception, s.demo, 2, 1, 2)
        s.parse('queryroutes.json')

