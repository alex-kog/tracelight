from unittest import TestCase

from query_routes_parser import QueryRoutesParser


class QueryRoutesParserTest(TestCase):
    def test_pars(self):
        s = QueryRoutesParser()

        s.parse('queryroutes.json')

