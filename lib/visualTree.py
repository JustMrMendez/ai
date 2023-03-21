import igraph as ig


def generate_igraph_data(tree, G=None, parent_vertex=None):
    if G is None:
        G = ig.Graph(directed=True)

    node_label = f"{tree['name']} ({tree['relative_path']})"
    vertex_id = G.vcount()
    G.add_vertex(name=node_label)

    if parent_vertex is not None:
        G.add_edge(parent_vertex, vertex_id)

    for file_info in tree['files']:
        file_label = f"{file_info['name']} ({file_info['relative_path']})"
        file_vertex_id = G.vcount()
        G.add_vertex(name=file_label,
                     last_modified=file_info['metadata']['last_modified'])
        G.add_edge(vertex_id, file_vertex_id)

    for subfolder in tree['subfolders']:
        generate_igraph_data(subfolder, G, vertex_id)

    return G


def visualize_tree(tree):
    G = generate_igraph_data(tree)
    layout = G.layout('kk')  # Use the Kamada-Kawai layout algorithm

    visual_style = {
        "vertex_size": 20,
        "vertex_label": G.vs["name"],
        "vertex_label_size": 10,
        "edge_arrow_size": 0.5,
        "layout": layout,
        "bbox": (1000, 1000),
        "margin": 20,
    }

    plot = ig.plot(G, **visual_style)
    return plot
