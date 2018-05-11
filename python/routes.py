# This file is part of TraceLight.
#
# TraceLight is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# TraceLight is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Toasty.  If not, see <http://www.gnu.org/licenses/>.


from gyp.common import OrderedSet

from lncli_helper import GetChannelInfoRunner, GetNodeInfoRunner, QueryRoutesRunner


class Route:
    def __init__(self):
        self.total_amt = -1
        self.total_fees = -1
        self.channels = []
        self.state = "UNKNOWN"

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

    def nodes(self, own_pub_key):
        nodes = OrderedSet([])
        for channel in self.channels:
            if (channel.node2.pub_key == own_pub_key):
                nodes.add(channel.node2)
                nodes.add(channel.node1)
            else:
                nodes.add(channel.node1)
                nodes.add(channel.node2)

        return nodes

    def __str__(self):
        s = '\n**Route**\nHops: %s\n' % (len(self.channels))
        s += '  Channels'
        for channel in self.channels:
            s += '\n        channel: ' + str(channel)
        return s


class Channel:
    def __init__(self):
        self.node1 = Node()
        self.node2 = Node()
        self.capacity = -1
        self.chan_id = -1
        self.state = "UNKNOWN"
        self.enough_capacity = False

    def decode(self, json):
        self.chan_id = json['chan_id']

    def __str__(self):
        return 'id: %s, capacity %s, node1: %s, node2: %s ' \
               % (self.chan_id,  self.capacity, self.node1, self.node2)


class Node:
    def __init__(self):
        self.weight = -1
        self.alias = ""
        self.pub_key = ""
        self.state = "UNKNOWN"

    def __str__(self):
        return 'alias: %-40s pub_key %-70s weight: %s ' \
               % (self.alias,  self.pub_key, self.weight)

    def __eq__(self, other):
        return self.pub_key == other.pub_key

    def __hash__(self):
        return hash(('pub_key', self.pub_key))


class RoutesFetcher:
    def __init__(self):
        pass

    def routes(self, dest):
        routes = QueryRoutesParser().parse(QueryRoutesRunner().result(dest, 1))
        for route in routes:
            self.populateChannelInfo(route, GetChannelInfoRunner(), GetNodeInfoRunner())

        return routes

    def populateChannelInfo(self, route, channelInfoRunner, nodeInfoRunner):
        for channel in route.channels:
            data = channelInfoRunner.result(channel)

            channel.node1.pub_key = data['node1_pub']
            channel.node2.pub_key = data['node2_pub']
            channel.capacity = data['capacity']

            data = nodeInfoRunner.result(channel.node1.pub_key)
            channel.node1.alias = data['node']['alias']

            data = nodeInfoRunner.result(channel.node2.pub_key)
            channel.node2.alias = data['node']['alias']


class QueryRoutesParser:
    def __init__(self):
        pass

    def parse(self, data):
        routes = []
        for route in data['routes']:
            r = Route()
            r.decode(route)
            routes.append(r)

        return routes






