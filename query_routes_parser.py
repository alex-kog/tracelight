import json

from gyp.common import OrderedSet


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

    def populateChannelInfo(self, channelInfoRunner, nodeInfoRunner):
        for channel in self.channels:
            with open('temp_channel_info.json', "w") as outfile:
                channelInfoRunner.run(channel.chan_id, outfile)
                outfile.close()

            with open('temp_channel_info.json') as data_file:
                data = json.load(data_file)
                channel.populateChannelInfo(data)
                data_file.close()

            with open('temp_node_info.json', "w") as outfile:
                nodeInfoRunner.run(channel.node1.pub_key, outfile)
                outfile.close()

            with open('temp_node_info.json') as data_file:
                data = json.load(data_file)
                channel.node1.alias = data['node']['alias']
                data_file.close()

            with open('temp_node_info.json', "w") as outfile:
                nodeInfoRunner.run(channel.node2.pub_key, outfile)
                outfile.close()

            with open('temp_node_info.json') as data_file:
                data = json.load(data_file)
                channel.node2.alias = data['node']['alias']
                data_file.close()

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
        self.enough_capacity = True

    def decode(self, json):
        self.chan_id = json['chan_id']

    def populateChannelInfo(self, data):
        self.node1.pub_key = data['node1_pub']
        self.node2.pub_key = data['node2_pub']
        self.capacity = data['capacity']

    def __str__(self):
        return 'id: %s, capacity %s, node1: %s, node2: %s ' \
               % (self.chan_id,  self.capacity, self.node1, self.node2)

    def getDestNode(self, own_pub_key):
        #TODO this is a hack
        if self.node2.pub_key == own_pub_key:
            return self.node1
        else:
            return self.node2

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






