# This file is part of TraceLight.
#
# TraceLight is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# TraceLight is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Toasty.  If not, see <http://www.gnu.org/licenses/>.


import json
import subprocess


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


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


def jsonData(filename):
    with open(filename) as data_file:
        data = json.load(data_file)
        data_file.close()
    return data


class GetInfoRunner:
    def __init__(self):
        pass

    def run(self, stdout=subprocess.PIPE):
        args = ["lncli", "getinfo"]
        return runCommand(args, stdout)

    def result(self):
        with open('temp.json', "w") as outfile:
            self.run(outfile)
            outfile.close()

        return jsonData('temp.json')


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

    def result(self, pubkey, amt):
        with open('temp.json', "w") as outfile:
            self.run(pubkey, amt, outfile)
            outfile.close()

        return jsonData('temp.json')


class GetChannelInfoRunner:
    def __init__(self):
        pass

    def run(self, channel, stdout=subprocess.PIPE):
        args = ["lncli", "getchaninfo", "{}".format(channel)]
        return runCommand(args, stdout)

    def result(self, channel):
        with open('temp.json', "w") as outfile:
            self.run(channel.chan_id, outfile)
            outfile.close()

        return jsonData('temp.json')


class GetNodeInfoRunner:
    def __init__(self):
        pass

    def run(self, pub_key, stdout=subprocess.PIPE):
        args = ["lncli", "getnodeinfo", "{}".format(pub_key)]
        return runCommand(args, stdout)

    def result(self, pub_key):
        with open('temp.json', "w") as outfile:
            self.run(pub_key, outfile)
            outfile.close()

        return jsonData('temp.json')


class QueryRoutesRunner:
    def __init__(self):
        pass

    def run(self, pubkey, amount, stdout=subprocess.PIPE):
        args = ["lncli", "queryroutes", "{}".format(pubkey), "{}".format(amount)]
        return runCommand(args, stdout)

    def result(self, pubkey, amount):
        with open('temp.json', "w") as outfile:
            self.run(pubkey, amount, outfile)
            outfile.close()

        return jsonData('temp.json')
