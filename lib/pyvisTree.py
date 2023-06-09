import hashlib
import os
from pyvis.network import Network


def generate_pyvis_data(tree, nt=None, parent_vertex=None, file_names=None, file_hashes=None):
    if nt is None:
        nt = Network(notebook=False, height="100vh", width="100%")
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

        # Default values for normal files
        file_color = 'lightblue'
        file_size = 20
        file_font_size = 14

        # Check for duplicated file names
        if file_info['name'] in file_names:
            file_color = 'red'
            file_size = 40
            file_font_size = 18
            file_names[file_info['name']].append(file_vertex_id)
        else:
            file_names[file_info['name']] = [file_vertex_id]

        # Check for duplicated file contents
        file_path = os.path.join(tree['folder_path'], file_info['name'])
        try:
            with open(file_path, 'rb') as f:
                file_hash = hashlib.md5(f.read()).hexdigest()

            if file_hash in file_hashes:
                file_color = 'blue'
                file_size = 40
                file_font_size = 18
                file_hashes[file_hash].append(file_vertex_id)
            else:
                file_hashes[file_hash] = [file_vertex_id]
        except FileNotFoundError:
            with open('errored.txt', 'a') as error_file:
                error_file.write(f"{file_path}\n")
            continue

        nt.add_node(file_vertex_id, label=file_label, title=f"{file_label}\nLast modified: {last_modified}",
                    color=file_color, size=file_size, font=dict(size=file_font_size))
        nt.add_edge(vertex_id, file_vertex_id)

    for subfolder in tree['subfolders']:
        generate_pyvis_data(subfolder, nt, vertex_id, file_names, file_hashes)

    return nt


def visualize_tree(tree):
    nt = generate_pyvis_data(tree)
    nt.show("tree_visualization.html", notebook=False)
