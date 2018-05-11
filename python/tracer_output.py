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


import collections
import json


class TraceOutput:
    def __init__(self, routes, amt, own_pub_key):
        self.routes = routes
        self.amount = amt
        self.own_pub_key = own_pub_key

    def outputToFile(self, filename):
        output = []
        own_node = list(self.routes[0].nodes(self.own_pub_key))[0]
        for index, route in enumerate(self.routes):
            ordered_route_nodes = list(route.nodes(self.own_pub_key))[1:]
            ordered_channels = route.channels

            route_data = collections.OrderedDict()
            dest = list(route.nodes(self.own_pub_key))[-1]
            route_data['route_id'] = index
            route_data['route_is_broken'] = True if route.state == "UNREACHABLE" else False

            hops = []
            for index, node in enumerate(ordered_route_nodes):
                channel = ordered_channels[index]
                hop = collections.OrderedDict()

                hop['chan_id'] = channel.chan_id
                hop['destination_pub'] = node.pub_key
                hop['destination_alias'] = node.alias
                hop['destination_status'] = node.state
                hop['enough_capacity'] = channel.enough_capacity
                hops.append(hop)

            route_data['hops'] = hops

            output.append(route_data)

        output_routes = collections.OrderedDict()
        output_routes['origin_pub'] = self.own_pub_key
        output_routes['origin_alias'] = own_node.alias
        output_routes['routes'] = output

        with open(filename, 'w') as outfile:
            s = json.dumps(output_routes, indent=4)
            outfile.write(s)
