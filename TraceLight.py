from lncli_helper import QueryRoutesRunner, GetChannelInfoRunner, GetNodeInfoRunner, SendPaymentRunner
from query_routes_parser import QueryRoutesParser
from routes_filter import RoutesFilter


def fetchRoutes(queryRoutes, routeParser, getChannelInfo, getNodeInfo):
    with open('temp_queryroutes.json', "w") as outfile:
        queryRoutes.run(1, outfile)
        outfile.close()

    routes = routeParser.parse('temp_queryroutes.json')
    for r in routes:
        r.populateChannelInfo(getChannelInfo, getNodeInfo)

    return routes


if __name__ == "__main__":
    queryRoutes = QueryRoutesRunner("02c8b565720eaa9c3819b7020c4ee7c084cb9f7a6cd347b006eae5e5698df9f490")
    sendPayment = SendPaymentRunner("02c8b565720eaa9c3819b7020c4ee7c084cb9f7a6cd347b006eae5e5698df9f490")
    routeParser = QueryRoutesParser()
    getChannelInfo = GetChannelInfoRunner()
    getNodeInfo = GetNodeInfoRunner()
    filterRoutes = RoutesFilter()

    routes = fetchRoutes(queryRoutes, routeParser, getChannelInfo, getNodeInfo)
    routes = filterRoutes.filter(routes, queryRoutes, sendPayment)

    for r in routes:
        print r

        # draw(routes[1].channels)
