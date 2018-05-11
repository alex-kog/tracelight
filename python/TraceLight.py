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


import argparse

from lncli_helper import GetInfoRunner
from tracer import Tracer
from tracer_output import TraceOutput
from routes import RoutesFetcher

class TraceLight:
    def __init__(self):
        pass

    def run(self, dest, amt, output_filename, quiet_mode, max_routes=100):
        own_pub_key = self.fetchOwnPubKey()
        routes = RoutesFetcher().routes(dest)

        Tracer(max_routes, quiet_mode).trace(routes, amt, own_pub_key)
        TraceOutput(routes, amt, own_pub_key).outputToFile(output_filename)

    def fetchOwnPubKey(self):
        data = GetInfoRunner().result()
        return data['identity_pubkey']


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-d', help='destination public key', dest='destination', default="")
    parser.add_argument('-a', help='amount', dest='amount', default="")
    parser.add_argument('-o', help='output', dest='output', default="output.json")
    parser.add_argument('-m', help='max_routes', dest='max_routes', default=10)
    parser.add_argument('-q', action="store_true", help='quiet mode', dest='quiet')
    args = parser.parse_args()

    dest = args.destination
    amount = args.amount
    output = args.output
    quiet = args.quiet
    max_routes = int(args.max_routes)

    TraceLight().run(dest, amount, 'output/%s' % output, quiet, max_routes)
