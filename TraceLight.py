import json
import subprocess
import sys

from query_routes_parser import QueryRoutesParser


def getchannelinfo(channel):
    args = ["lncli", "getchaninfo", "{}".format(channel)]
    return runCommand(args)

def queryroutes(stdout, pub, amount):
    args = ["lncli", "queryroutes", "{}".format(pub), "{}".format(amount)]
    return runCommand(args, stdout)


def sendPayment(pub, amt):
    args = ["lncli", "sendpayment", "--dest", "{}".format(pub), "--amt", "{}".format(amt), "--final_cltv_delta",
            "{}".format(144)
        , "--payment_hash",
            "f4765e0acbee6687e19292204d2aaa72d3f10642253144a292ab66613c123456"]

    return runCommand(args)


def runCommand(args, stdout = subprocess.PIPE):
    exitOnError = True
    printError = True
    shell = False
    try:
        process = subprocess.Popen(args, stdout=stdout, stderr=subprocess.PIPE, shell=shell)
        out, err = process.communicate()
        if (err):
            if (printError == True):
                print err
            if (exitOnError == True and "Note" not in err):
                exit(1)

        return out, err
    except OSError as e:
        print "Exception: " + str(e)
        print e.filename
        raise


if __name__ == "__main__":
    # #testing
    # print sendPayment("02c8b565720eaa9c3819b7020c4ee7c084cb9f7a6cd347b006eae5e5698df9f490", 1)
    # print getchannelinfo("1425805996972179456")

    with open('queryroutes.json', "w") as outfile:
        queryroutes(outfile, "02c8b565720eaa9c3819b7020c4ee7c084cb9f7a6cd347b006eae5e5698df9f490", 1)
        outfile.close()
    queryRouteParser = QueryRoutesParser()
    routes = queryRouteParser.parse('queryroutes.json')

    for r in routes:
        print r