from lncli_helper import QueryRoutesRunner, GetChannelInfoRunner, GetNodeInfoRunner, SendPaymentRunner
from query_routes_parser import QueryRoutesParser
from routes_filter import RoutesFilter

class Tracer:
    def __init__(self, sendPayment):
        self.sendPayment = sendPayment

    # def trace(self, routes, value):
    #     for route in routes:
    #         route_is_broken = False
    #         minimal_capacity = False
    #         for index, channel in enumerate(route.channels):
    #             if route_is_broken:
    #                 route.state = "UNREACHABLE"
    #                 break
    #             amount = 1 if minimal_capacity else value
    #
    #             with open('temp_sendPayment.json', "w") as outfile:
    #                 self.sendPayment.run(amount, outfile)
    #                 outfile.close()





class TraceLight:
    def __init__(self):
        self.queryRoutes = QueryRoutesRunner("02c8b565720eaa9c3819b7020c4ee7c084cb9f7a6cd347b006eae5e5698df9f490")
        self.sendPayment = SendPaymentRunner()
        self.routeParser = QueryRoutesParser()
        self.getChannelInfo = GetChannelInfoRunner()
        self.getNodeInfo = GetNodeInfoRunner()
        self.filterRoutes = RoutesFilter()

    def run(self):
        self.fetchQueryRoutes(self.queryRoutes)
        routes = self.fetchRoutes(self.routeParser, self.getChannelInfo, self.getNodeInfo)
        routes = self.filterRoutes.filter(routes, self.queryRoutes, self.sendPayment)

        for r in routes:
            print r

    def fetchQueryRoutes(self, queryRoutes):
        with open('temp_queryroutes.json', "w") as outfile:
            queryRoutes.run(1, outfile)
            outfile.close()

    def fetchRoutes(self, routeParser, getChannelInfo, getNodeInfo):
        routes = routeParser.parse('temp_queryroutes.json')
        for r in routes:
            r.populateChannelInfo(getChannelInfo, getNodeInfo)

        return routes


if __name__ == "__main__":
    TraceLight().run()
