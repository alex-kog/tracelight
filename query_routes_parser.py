import json
import math
from pprint import pprint


class Route:
    def decode(self, json):
        self.total_amt = json['total_amt']
        self.total_fees = json['total_fees']
        self.hops = self.decodeHops(json['hops'])

    def decodeHops(self, json):
        hops = []
        for hop in json:
            h = Hop()
            h.decode(hop)
            hops.append(h)
        return hops

    def __str__(self):
        s = '\n**Route**\ncount: %s\n' % (len(self.hops))
        s += '  Hops'
        for hop in self.hops:
            s += '\n        chan_id: ' + str(hop)
        return s


class Hop:
    def decode(self, json):
        self.chan_id = json['chan_id']

    def __str__(self):
        return str(self.chan_id)


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
