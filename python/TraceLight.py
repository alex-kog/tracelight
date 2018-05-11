import argparse

from lncli_helper import GetInfoRunner
from python.tracer import Tracer
from python.tracer_output import TraceOutput
from routes import RoutesFetcher


class TraceLight:
    def __init__(self):
        pass

    def run(self, dest, amt, output_filename, max_routes=100):
        own_pub_key = self.fetchOwnPubKey()
        routes = RoutesFetcher().routes(dest)

        Tracer().trace(routes, amt, own_pub_key, max_routes)
        TraceOutput(routes, amt, own_pub_key).outputToFile(output_filename)

    def fetchOwnPubKey(self):
        data = GetInfoRunner().result()
        return data['identity_pubkey']


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
