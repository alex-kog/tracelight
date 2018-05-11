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


import networkx as nx
import matplotlib.pyplot as plt


# edge [u,v,w]


def draw_routes(routes):
    start = routes[0].channels[0].node1.alias
    end = routes[0].channels[-1].node2.alias

    inodes = [start, end]
    nodes = set()
    for route in routes:
        for channel in route.channels:
            nodes.add(channel.node1.alias)
            nodes.add(channel.node2.alias)

    G = nx.MultiGraph()
    G.add_nodes_from(nodes)

    pos = nx.spring_layout(G)  # positions for all nodes

    edgelables = {}
    for route in routes:
        extract_info(G, pos, route, edgelables)

    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=500)

    # edges
    nx.draw_networkx_edges(G, pos,
                           width=1, alpha=0.5, edge_color='b')

    # labels
    nx.draw_networkx_labels(G, pos, font_size=10, font_color='g', font_family='sans-serif')

    plt.axis('off')
    plt.show()


def extract_info(G, pos, route, edge_labels):
    import random
    r = lambda: random.randint(0, 255)

    edges = []
    for channel in route.channels:
        edges.append((channel.node1.alias, channel.node2.alias))
        G.add_edge(channel.node1.alias, channel.node2.alias)
        edge_labels[(channel.node1.alias, channel.node2.alias)] = \
            "node: {}, weight: {}\n node: {}, weight: {}" \
                .format(channel.node1.alias, channel.node1.weight, channel.node2.alias, channel.node1.weight)

    color = '#%02X%02X%02X' % (r(), r(), r())
    nx.draw_networkx_edges(G, pos, edges, arrows=True,
                           width=1, alpha=0.5, edge_color=color)
