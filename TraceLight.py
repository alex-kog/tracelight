import argparse
import json

import collections

from lncli_helper import QueryRoutesRunner, GetChannelInfoRunner, GetNodeInfoRunner, SendPaymentRunner, GetInfoRunner, \
    bcolors
from query_routes_parser import QueryRoutesParser


class Tracer:
    def __init__(self):
        pass

    def trace(self, routes, amt, own_pub_key, max_routes):
        offline_nodes = []
        no_capacity_nodes = []

        for index, route in enumerate(routes):
            if index == max_routes:
                break

            print '%s\n\nCHECKING ROUTE #%s\n%s' % (bcolors.OKBLUE, index, bcolors.ENDC)
            route_is_broken = False
            minimal_capacity = False
            ordered_route_nodes = list(route.nodes(own_pub_key))[1:]
            ordered_channels = route.channels

            for index, node in enumerate(ordered_route_nodes):
                if node.state == "OFFLINE":
                    route_is_broken = True
                    continue

                if route_is_broken:
                    route.state = "UNREACHABLE"
                    break

                channel = ordered_channels[index]
                amount = 1 if minimal_capacity else amt

                print '%s*** TESTING ***%s' % (bcolors.WARNING, bcolors.ENDC)
                print 'FROM: %-25s %s' % ("YOU", own_pub_key)
                print 'TO  : %-25s %s' % (node.alias, node.pub_key)
                print 'AMOUNT: %s' % amount

                if node in offline_nodes:
                    result = "timeout"
                else:
                    result = self.sendPayment(node.pub_key, amount)

                color = bcolors.FAIL
                should_break = True
                if 'timeout' in result or \
                                'UnknownNextPeer' in result or \
                                'unable to find a path' in result:
                    status = "NODE IS OFFLINE"
                    channel.state = "NO CHANNEL - DEST NODE OFFLINE"
                    channel.enough_capacity = False
                    node.state = "OFFLINE"
                    offline_nodes.append(node)
                    route_is_broken = True

                elif "TemporaryChannelFailure" in result:
                    status = "NOT ENOUGH CAPACITY"
                    channel.state = "NOT ENOUGH CAPACITY"
                    node.state = "ONLINE"
                    no_capacity_nodes.append(node)
                    channel.enough_capacity = False
                    minimal_capacity = True
                    should_break = False

                elif "UnknownPaymentHash" in result:  # This means money went through
                    status = "SUCCESS" if amount == amt else "LIVE"
                    channel.state = "ACTIVE" if amount == amt else "NOT ENOUGH CAPACITY"
                    channel.enough_capacity = True if amount == amt else False
                    node.state = "ONLINE"
                    color = bcolors.OKGREEN
                    should_break = False
                    result = ""
                else:
                    status = "FUCK"

                print 'RESULT: %s%s%s %s\n' % \
                      (color, status, bcolors.ENDC, "" if result == "" else '(%s)' % result)

                if should_break:
                    break

    def sendPayment(self, pubkey, amount):
        with open('temp_sendPayment.json', "w") as outfile:
            SendPaymentRunner().run(pubkey, amount, outfile)
            outfile.close()

        return self.parsePaymentResult('temp_sendPayment.json')

    def parsePaymentResult(self, filename):
        with open(filename) as data_file:
            data = json.load(data_file)
            # print data
            result = data['payment_error']
            data_file.close()
        return result

class TraceOutput:
    def __init__(self, routes, amt, own_pub_key):
        self.routes = routes
        self.amount = amt
        self.own_pub_key = own_pub_key

    def outputToFile(self, filename):
        output = []
        own_node = list(self.routes[0].nodes(self.own_pub_key))[0]
        for index, route in enumerate(self.routes):
            ordered_route_nodes = list(route.nodes(self.own_pub_key))[1:]
            ordered_channels = route.channels

            route_data = collections.OrderedDict()
            dest = list(route.nodes(self.own_pub_key))[-1]
            route_data['route_id'] = index
            route_data['route_is_broken'] = True if route.state == "UNREACHABLE" else False

            hops = []
            for index, node in enumerate(ordered_route_nodes):
                channel = ordered_channels[index]
                hop = collections.OrderedDict()

                hop['chan_id'] = channel.chan_id
                hop['destination_pub'] = node.pub_key
                hop['destination_alias'] = node.alias
                hop['destination_status'] = node.state
                hop['enough_capacity'] = channel.enough_capacity
                hops.append(hop)

            route_data['hops'] = hops

            output.append(route_data)

        output_routes = collections.OrderedDict()
        output_routes['origin_pub'] = self.own_pub_key
        output_routes['origin_alias'] = own_node.alias
        output_routes['routes'] = output



        with open(filename, 'w') as outfile:
            s = json.dumps(output_routes, indent=4)
            outfile.write(s)



class TraceLight:
    def __init__(self):
        pass

    def run(self, dest, amt, output_filename, max_routes = 100):
        own_pub_key = self.fetchOwnPubKey()
        self.fetchQueryRoutes(dest)
        routes = self.fetchRoutes()

        Tracer().trace(routes, amt, own_pub_key, max_routes)
        TraceOutput(routes, amt, own_pub_key).outputToFile(output_filename)

    def fetchOwnPubKey(self):
        with open('temp_getinfo.json', "w") as outfile:
            GetInfoRunner().run(outfile)
            outfile.close()

        with open('temp_getinfo.json') as data_file:
            data = json.load(data_file)
            data_file.close()

        return data['identity_pubkey']

    def fetchQueryRoutes(self, dest):
        with open('temp_queryroutes.json', "w") as outfile:
            QueryRoutesRunner().run(dest, 1, outfile)
            outfile.close()

    def fetchRoutes(self):
        routeParser = QueryRoutesParser()
        getChannelInfo = GetChannelInfoRunner()
        getNodeInfo = GetNodeInfoRunner()
        routes = routeParser.parse('temp_queryroutes.json')
        for r in routes:
            r.populateChannelInfo(getChannelInfo, getNodeInfo)

        return routes


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-d', help='destination public key', dest='destination', default="")
    parser.add_argument('-a', help='amount', dest='amount', default="")
    parser.add_argument('-o', help='output', dest='output', default="output.json")
    args = parser.parse_args()

    dest = args.destination
    amount = args.amount
    output = args.output

    TraceLight().run(dest, amount, 'output/%s' % output)
