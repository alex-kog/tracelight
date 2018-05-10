import subprocess


def runCommand(args, stdout=subprocess.PIPE):
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


class SendPaymentRunner:
    def __init__(self):
        pass

    def run(self, pubkey, amt, stdout=subprocess.PIPE):
        args = ["lncli", "sendpayment",
                "--dest", "{}".format(pubkey),
                "--amt", "{}".format(amt),
                "--final_cltv_delta", "{}".format(144),
                "--payment_hash", "f4765e0acbee6687e19292204d2aaa72d3f10642253144a292ab66613c123456"]

        return runCommand(args, stdout)


class GetChannelInfoRunner:
    def __init__(self):
        pass

    def run(self, channel, stdout=subprocess.PIPE):
        args = ["lncli", "getchaninfo", "{}".format(channel)]
        return runCommand(args, stdout)


class GetNodeInfoRunner:
    def __init__(self):
        pass

    def run(self, channel, stdout=subprocess.PIPE):
        args = ["lncli", "getnodeinfo", "{}".format(channel)]
        return runCommand(args, stdout)


class QueryRoutesRunner:
    def __init__(self, pubkey):
        self.pubkey = pubkey

    def run(self, amount, stdout=subprocess.PIPE):
        args = ["lncli", "queryroutes", "{}".format(self.pubkey), "{}".format(amount)]
        return runCommand(args, stdout)
