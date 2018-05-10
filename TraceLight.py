import json
import subprocess
import sys

from draw_graph import draw
from lncli_helper import QueryRoutesRunner, GetChannelInfoRunner, GetNodeInfoRunner
from query_routes_parser import QueryRoutesParser


def fetchRoutes(queryRoutesRunner, queryRouteParser, channelInfoRunner, nodeInfoRunner):
    with open('temp_queryroutes.json', "w") as outfile:
        queryRoutesRunner.run(1, outfile)
        outfile.close()

    routes = queryRouteParser.parse('temp_queryroutes.json')
    for r in routes:
        r.populateChannelInfo(channelInfoRunner, nodeInfoRunner)

    return routes


if __name__ == "__main__":
    queryRoutesRunner = QueryRoutesRunner("02c8b565720eaa9c3819b7020c4ee7c084cb9f7a6cd347b006eae5e5698df9f490")
    queryRouteParser = QueryRoutesParser()
    channelInfoRunner = GetChannelInfoRunner()
    nodeInfoRunner = GetNodeInfoRunner()

    routes = fetchRoutes(queryRoutesRunner, queryRouteParser, channelInfoRunner, nodeInfoRunner)

    for r in routes:
        print r

        # draw(routes[1].channels)
