import json
import math
from pprint import pprint

from lncli_helper import GetChannelInfoRunner


class Route:
    def decode(self, json):
        self.total_amt = json['total_amt']
        self.total_fees = json['total_fees']
        self.channels = self.decodeHops(json['hops'])

    def decodeHops(self, json):
        hops = []
        for channel in json:
            h = Channel()
            h.decode(channel)
            hops.append(h)
        return hops

    def __str__(self):
        s = '\n**Route**\nHops: %s\n' % (len(self.channels))
        s += '  Channels'
        for channel in self.channels:
            s += '\n        channel: ' + str(channel)
        return s


class Channel:
    def __init__(self):
        self.node1_weight = -1
        self.node2_weight = -1
        self.node1_alias = ""
        self.node2_alias = ""

    def decode(self, json):
        self.chan_id = json['chan_id']

    def populateChannelInfo(self, data):
        self.node1_pub = data['node1_pub']
        self.node2_pub = data['node2_pub']
        self.capacity = data['capacity']

    def __str__(self):
        return 'id: %s, node1_pub: %s, node2_pub: %s, capacity %s, node1_weight: %s, node2_weight: %s, node1_alias: %s, node2_alias: %s' \
               % (self.chan_id, self.node1_pub, self.node2_pub, self.capacity, self.node1_weight, self.node2_weight, self.node1_alias, self.node2_alias)


class QueryRoutesParser:
    def __init__(self):
        pass

    def parse(self, json_file):
        with open(json_file) as data_file:
            data = json.load(data_file)

        routes = []
        for route in data['routes']:
            r = Route()
            r.decode(route)
            routes.append(r)

        return routes



