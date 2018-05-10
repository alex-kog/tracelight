import json

from lncli_helper import QueryRoutesRunner, GetChannelInfoRunner, GetNodeInfoRunner, SendPaymentRunner, GetInfoRunner, \
    bcolors
from query_routes_parser import QueryRoutesParser


class Tracer:
    def __init__(self):
        pass

    def trace(self, routes, amt, own_pub_key):
        for index, route in enumerate(routes):
            print '%s\n\nCHECKING ROUTE #%s\n%s' % (bcolors.OKBLUE , index, bcolors.ENDC)
            route_is_broken = False
            minimal_capacity = False
            ordered_route_nodes = list(route.nodes(own_pub_key))[1:]

            for node in ordered_route_nodes:
                if node.state == "DEAD":
                    route_is_broken = True
                    continue

                print '%s*** TESTING ***%s' % (bcolors.WARNING, bcolors.ENDC)
                print 'FROM: %-25s %s' % ("YOU", own_pub_key)
                print 'TO  : %-25s %s' % (node.alias, node.pub_key)

                if route_is_broken:
                    route.state = "UNREACHABLE"
                    break

                amount = 1 if minimal_capacity else amt

                print 'AMOUNT: %s' % amount

                result = self.sendPayment(node.pub_key, amount)

                color = bcolors.FAIL
                if 'timeout' in result or 'UnknownNextPeer' in result:
                    result = "NODE IS OFFLINE"
                    route_is_broken = True

                elif "TemporaryChannelFailure" in result:
                    node.state = "DEAD"
                    minimal_capacity = True
                    result = "NOT ENOUGH CAPACITY"

                elif "UnknownPaymentHash" in result:  # This means money went through
                    node.state = "ONLINE"
                    result = "SUCCESS"
                    color = bcolors.OKGREEN
                else:
                    result = "FUCK"

                print 'RESULT: %s%s%s' % (color, result, bcolors.ENDC)
                print '*********************************\n'

                if result is not "SUCCESS":
                    break

    def sendPayment(self, pubkey, amount):
        with open('temp_sendPayment.json', "w") as outfile:
            SendPaymentRunner().run(pubkey, amount, outfile)
            outfile.close()

        return self.parsePaymentResult('temp_sendPayment.json')

    def parsePaymentResult(self, filename):
        result = ""
        with open(filename) as data_file:
            data = json.load(data_file)
            # print data
            result = data['payment_error']
            data_file.close()
        return result


class TraceLight:
    def __init__(self):
        pass

    def run(self, dest, amt):
        own_pub_key = self.fetchOwnPubKey()
        self.fetchQueryRoutes(dest)
        routes = self.fetchRoutes()

        Tracer().trace(routes, amt, own_pub_key)

    def fetchOwnPubKey(self):
        with open('temp_getinfo.json', "w") as outfile:
            GetInfoRunner().run(outfile)
            outfile.close()

        data = {}
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
    TraceLight().run('02c8b565720eaa9c3819b7020c4ee7c084cb9f7a6cd347b006eae5e5698df9f490', 1000)
