from unittest import TestCase

from TraceLight import TraceLight
from lncli_helper import GetChannelInfoRunner, GetNodeInfoRunner
from query_routes_parser import QueryRoutesParser


class TraceLightTest(TestCase):
    def test_pars(self):
        tl = TraceLight()
        self.routeParser = QueryRoutesParser()
        self.getChannelInfo = GetChannelInfoRunner()
        self.getNodeInfo = GetNodeInfoRunner()

        routes = tl.fetchRoutes(self.routeParser, self.getChannelInfo, self.getNodeInfo)


        for r in routes:
            print r