import subprocess
import sys

def getchannelinfo(channel):
    args = ["lncli", "getchaninfo", "{}".format(channel)]
    return runCommand(args)

def queryroutes(pub):
    args = ["lncli", "queryroutes", "{}".format(pub), "1"]
    return runCommand(args)


def sendPayment(pub, amt):
    args = ["lncli", "sendpayment", "--dest", "{}".format(pub), "--amt", "{}".format(amt), "--final_cltv_delta",
            "{}".format(144)
        , "--payment_hash",
            "f4765e0acbee6687e19292204d2aaa72d3f10642253144a292ab66613c123456"]

    return runCommand(args)


def runCommand(args):
    exitOnError = True
    printError = True
    shell = False
    try:
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell)
        out, err = process.communicate()
        if (err):
            if (printError == True):
                print err
            if (exitOnError == True and "Note" not in err):
                exit(1)

        return out.strip(), err
    except OSError as e:
        print "Exception: " + str(e)
        print e.filename
        raise


if __name__ == "__main__":
    #testing
    print sendPayment("02c8b565720eaa9c3819b7020c4ee7c084cb9f7a6cd347b006eae5e5698df9f490", 1)
    print queryroutes("02c8b565720eaa9c3819b7020c4ee7c084cb9f7a6cd347b006eae5e5698df9f490")
    print getchannelinfo("1425805996972179456")