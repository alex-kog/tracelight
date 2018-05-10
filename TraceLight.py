import json
import subprocess
import sys

from lncli_helper import QueryRoutesRunner
from query_routes_parser import QueryRoutesParser

if __name__ == "__main__":
    # #testing
    # print sendPayment("02c8b565720eaa9c3819b7020c4ee7c084cb9f7a6cd347b006eae5e5698df9f490", 1)
    # print getchannelinfo("1425805996972179456")



    with open('queryroutes.json', "w") as outfile:
        QueryRoutesRunner("02c8b565720eaa9c3819b7020c4ee7c084cb9f7a6cd347b006eae5e5698df9f490").run(1, outfile)
        outfile.close()
    queryRouteParser = QueryRoutesParser()
    routes = queryRouteParser.parse('queryroutes.json')

    for r in routes:
        print r
