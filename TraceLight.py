import json
import subprocess
import sys

from lncli_helper import QueryRoutesRunner, GetChannelInfoRunner, GetNodeInfoRunner
from query_routes_parser import QueryRoutesParser


def queryMainRoute(pubkey):
    with open('temp_queryroutes.json', "w") as outfile:
        QueryRoutesRunner(pubkey).run(1, outfile)
        outfile.close()
    queryRouteParser = QueryRoutesParser()
    routes = queryRouteParser.parse('temp_queryroutes.json')
    return routes


def populateChannelInfo(route):
    channelInfoRunner = GetChannelInfoRunner()
    nodeInfoRunner = GetNodeInfoRunner()
    for channel in route.channels:
        with open('temp_channel_info.json', "w") as outfile:
            channelInfoRunner.run(channel.chan_id, outfile)
            outfile.close()

        with open('temp_channel_info.json') as data_file:
            data = json.load(data_file)
            channel.populateChannelInfo(data)
            data_file.close()

        with open('temp_node_info.json', "w") as outfile:
            nodeInfoRunner.run(channel.node1_pub, outfile)
            outfile.close()

        with open('temp_node_info.json') as data_file:
            data = json.load(data_file)
            channel.node1_alias = data['node']['alias']
            data_file.close()

        with open('temp_node_info.json', "w") as outfile:
            nodeInfoRunner.run(channel.node2_pub, outfile)
            outfile.close()

        with open('temp_node_info.json') as data_file:
            data = json.load(data_file)
            channel.node2_alias = data['node']['alias']
            data_file.close()




if __name__ == "__main__":
    routes = queryMainRoute('02c8b565720eaa9c3819b7020c4ee7c084cb9f7a6cd347b006eae5e5698df9f490')
    for r in routes:
        populateChannelInfo(r)
        print r
