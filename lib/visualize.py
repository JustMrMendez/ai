import plotly.graph_objects as go
import networkx as nx
import matplotlib.pyplot as plt


def generate_sunburst_data(tree):
    ids = [tree['relative_path']]
    labels = [tree['name']]
    parents = [""]

    for file_info in tree['files']:
        ids.append(file_info['relative_path'])
        labels.append(file_info['name'])
        parents.append(tree['relative_path'])

    for subfolder in tree['subfolders']:
        sub_ids, sub_labels, sub_parents = generate_sunburst_data(subfolder)
        ids.extend(sub_ids)
        labels.extend(sub_labels)
        parents.extend(sub_parents)

    return ids, labels, parents


def pie_chart(tree):
    ids, labels, parents = generate_sunburst_data(tree)

    fig = go.Figure(go.Sunburst(
        ids=ids,
        labels=labels,
        parents=parents,
        branchvalues="total",
    ))

    fig.update_layout(
        margin=dict(t=0, l=0, r=0, b=0),
        title="Folder Structure",
    )

    fig.show()


def generate_graph_data(tree, G=None):
    if G is None:
        G = nx.DiGraph()

    node_label = f"{tree['name']} ({tree['relative_path']})"

    G.add_node(node_label)

    for file_info in tree['files']:
        file_label = f"{file_info['name']} ({file_info['relative_path']})"
        G.add_node(file_label)
        G.add_edge(node_label, file_label, type='file')
        G.nodes[file_label]['last_modified'] = file_info['metadata']['last_modified']

    for subfolder in tree['subfolders']:
        subfolder_node_label = generate_graph_data(subfolder, G)
        G.add_edge(node_label, subfolder_node_label, type='folder')

    return node_label


def tree_graph(tree):
    G = nx.DiGraph()
    generate_graph_data(tree, G)

    pos = nx.spring_layout(G)
    edge_labels = nx.get_edge_attributes(G, 'type')

    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=2000)
    nx.draw_networkx_edges(G, pos, edge_color='gray', width=2)
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels=edge_labels, font_color='red')
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='sans-serif')

    plt.axis('off')
    plt.title("Folder Structure")
    plt.show()