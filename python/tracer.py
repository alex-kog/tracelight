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


from lncli_helper import bcolors, SendPaymentRunner


class Tracer:
    def __init__(self, max_routes, quiet_mode):
        self.payment_cache = {}
        self.quiet_mode = quiet_mode
        self.max_routes = max_routes
        pass

    def log(self, str):
        if not self.quiet_mode:
            print str

    def trace(self, routes, amt, own_pub_key):
        offline_nodes = []
        no_capacity_nodes = []

        for index, route in enumerate(routes):
            if index == self.max_routes:
                break

            self.log('%s\n\nCHECKING ROUTE #%s\n%s' % (bcolors.OKBLUE, index, bcolors.ENDC))
            route_is_broken = False
            minimal_capacity = False
            ordered_route_nodes = list(route.nodes(own_pub_key))[1:]
            ordered_channels = route.channels

            for index, node in enumerate(ordered_route_nodes):
                if node.state == "OFFLINE":
                    route_is_broken = True
                    continue

                if route_is_broken:
                    route.state = "UNREACHABLE"
                    break

                channel = ordered_channels[index]
                amount = 1 if minimal_capacity else amt

                self.log('%s*** TESTING ***%s' % (bcolors.WARNING, bcolors.ENDC))
                self.log('FROM: %-25s %s' % ("YOU", own_pub_key))
                self.log('TO  : %-25s %s' % (node.alias, node.pub_key))
                self.log('AMOUNT: %s' % amount)

                if node in offline_nodes:
                    result = "timeout"
                else:
                    result = self.sendPayment(node.pub_key, amount)

                color = bcolors.FAIL
                should_break = True
                if 'timeout' in result or \
                                'UnknownNextPeer' in result or \
                                'unable to find a path' in result:
                    status = "NODE IS OFFLINE"
                    channel.state = "NO CHANNEL - DEST NODE OFFLINE"
                    channel.enough_capacity = False
                    node.state = "OFFLINE"
                    offline_nodes.append(node)
                    route_is_broken = True

                elif "TemporaryChannelFailure" in result:
                    status = "NOT ENOUGH CAPACITY"
                    channel.state = "NOT ENOUGH CAPACITY"
                    node.state = "ONLINE"
                    no_capacity_nodes.append(node)
                    channel.enough_capacity = False
                    minimal_capacity = True
                    should_break = False

                elif "UnknownPaymentHash" in result:  # This means money went through
                    status = "SUCCESS" if amount == amt else "LIVE"
                    channel.state = "ACTIVE" if amount == amt else "NOT ENOUGH CAPACITY"
                    channel.enough_capacity = True if amount == amt else False
                    node.state = "ONLINE"
                    color = bcolors.OKGREEN
                    should_break = False
                    result = ""
                else:
                    status = "FUCK"

                self.log('RESULT: %s%s%s %s\n' % \
                         (color, status, bcolors.ENDC, "" if result == "" else '(%s)' % result))

                if should_break:
                    break

    def sendPayment(self, pubkey, amount):
        if (pubkey, amount) in self.payment_cache.keys():
            return self.payment_cache[(pubkey, amount)]

        data = SendPaymentRunner().result(pubkey, amount)
        result = data['payment_error']
        self.payment_cache[(pubkey, amount)] = result
        return result
