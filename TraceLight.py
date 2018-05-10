import json
import subprocess
import sys

from lncli_helper import QueryRoutesRunner, GetChannelInfoRunner
from query_routes_parser import QueryRoutesParser


def queryMainRoute(pubkey):
    with open('queryroutes.json', "w") as outfile:
        QueryRoutesRunner(pubkey).run(1, outfile)
        outfile.close()
    queryRouteParser = QueryRoutesParser()
    routes = queryRouteParser.parse('queryroutes.json')
    return routes


def populateChannelInfo(route):
    runner = GetChannelInfoRunner()
    for channel in route.channels:
        with open('temp_channel_info.json', "w") as outfile:
            runner.run(channel.chan_id, outfile)
            outfile.close()

        with open('temp_channel_info.json') as data_file:
            data = json.load(data_file)
            channel.populateChannelInfo(data)


if __name__ == "__main__":
    routes = queryMainRoute('02c8b565720eaa9c3819b7020c4ee7c084cb9f7a6cd347b006eae5e5698df9f490')
    for r in routes:
        populateChannelInfo(r)
        print r
