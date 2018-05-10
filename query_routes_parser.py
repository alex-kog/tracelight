import json


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

    def nodes(self):
        nodes = []
        for channel in self.channels:
            nodes.append(channel.node1)
            nodes.append(channel.node2)
        return list(set(nodes))

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

    def decode(self, json):
        self.chan_id = json['chan_id']

    def populateChannelInfo(self, data):
        self.node1.pub_key = data['node1_pub']
        self.node2.pub_key = data['node2_pub']
        self.capacity = data['capacity']

    def __str__(self):
        return 'id: %s, capacity %s, node1: %s, node2: %s ' \
               % (self.chan_id,  self.capacity, self.node1, self.node2)


class Node:
    def __init__(self):
        self.weight = -1
        self.alias = ""
        self.pub_key = ""

    def __str__(self):
        return 'alias: %s, pub_key %s, weight: %s ' \
               % (self.alias,  self.pub_key, self.weight)


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






