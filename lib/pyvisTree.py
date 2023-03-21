from pyvis.network import Network


def generate_pyvis_data(tree, nt=None, parent_vertex=None, file_names=None, file_hashes=None):
    if nt is None:
        nt = Network(notebook=True)
        nt.set_options("""
        var options = {
          "edges": {
            "color": {
              "inherit": true
            },
            "smooth": false
          },
          "physics": {
            "minVelocity": 0.75
          }
        }
        """)
        file_names = {}
        file_hashes = {}

    node_label = f"{tree['name']} ({tree['relative_path']})"
    vertex_id = len(nt.nodes)

    nt.add_node(vertex_id, label=node_label, title=node_label)

    if parent_vertex is not None:
        nt.add_edge(parent_vertex, vertex_id)

    for file_info in tree['files']:
        file_label = f"{file_info['name']} ({file_info['relative_path']})"
        file_vertex_id = len(nt.nodes)
        last_modified = file_info['metadata']['last_modified']

        # Check for duplicated file names
        if file_info['name'] in file_names:
            file_color = 'red'
            file_names[file_info['name']].append(file_vertex_id)
        else:
            file_color = 'lightblue'
            file_names[file_info['name']] = [file_vertex_id]

        # Check for duplicated file contents
        file_path = os.path.join(tree['relative_path'], file_info['name'])
        with open(file_path, 'rb') as f:
            file_hash = hashlib.md5(f.read()).hexdigest()

        if file_hash in file_hashes:
            file_color = 'blue'
            file_hashes[file_hash].append(file_vertex_id)
        else:
            file_hashes[file_hash] = [file_vertex_id]

        nt.add_node(file_vertex_id, label=file_label,
                    title=f"{file_label}\nLast modified: {last_modified}", color=file_color)
        nt.add_edge(vertex_id, file_vertex_id)

    for subfolder in tree['subfolders']:
        generate_pyvis_data(subfolder, nt, vertex_id, file_names, file_hashes)

    return nt


def visualize_tree(tree):
    nt = generate_pyvis_data(tree)
    nt.show("tree_visualization.html")
