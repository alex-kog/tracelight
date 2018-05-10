import matplotlib.pyplot as plt
import networkx as nx


# edge [u,v,w]
def draw(channels):
    G = nx.Graph()

    dic_labels = {}
    for channel in channels:
        G.add_edge(channel.node1_pub, channel.node2_pub)
        dic_labels[(channel.node1_pub, channel.node2_pub)] = \
            "node: {}, weight: {}\n node: {}, weight: {}"\
                .format(channel.node1_alias, channel.node1_weight, channel.node2_alias, channel.node1_weight)

    pos = nx.spring_layout(G)  # positions for all nodes

    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=700)

    nx.draw_networkx_edges(G, pos, width=6)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=dic_labels)

    plt.axis('off')
    plt.show()
