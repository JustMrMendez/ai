import os
import time


def get_file_metadata(file_path):
    file_stats = os.stat(file_path)
    metadata = {
        'size': file_stats.st_size,
        'last_modified': time.ctime(file_stats.st_mtime),
    }
    return metadata


def generate_tree2(folder_path, relative_path=""):
    tree = {}
    if os.path.isdir(folder_path):
        tree['type'] = 'folder'
        tree['name'] = os.path.basename(folder_path)
        tree['relative_path'] = relative_path
        # Add folder_path to the tree structure
        tree['folder_path'] = folder_path
        tree['files'] = []
        tree['subfolders'] = []

        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            item_relative_path = os.path.join(relative_path, item)

            if os.path.isdir(item_path):
                subfolder_tree = generate_tree(item_path, item_relative_path)
                tree['subfolders'].append(subfolder_tree)
            else:
                file_info = {
                    'name': item,
                    'relative_path': item_relative_path,
                    'metadata': get_file_metadata(item_path),
                }
                tree['files'].append(file_info)
    else:
        print("Error: The provided path is not a folder!")

    return tree


def generate_tree(folder_path, relative_path="", duplicates=None):
    if duplicates is None:
        duplicates = {}

    tree = {}
    if os.path.isdir(folder_path):
        tree['type'] = 'folder'
        tree['name'] = os.path.basename(folder_path)
        tree['relative_path'] = relative_path
        tree['folder_path'] = folder_path
        tree['files'] = []
        tree['subfolders'] = []

        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            item_relative_path = os.path.join(relative_path, item)

            if os.path.isdir(item_path):
                subfolder_tree = generate_tree(
                    item_path, item_relative_path, duplicates)
                tree['subfolders'].append(subfolder_tree)
            else:
                file_info = {
                    'name': item,
                    'relative_path': item_relative_path,
                    'metadata': get_file_metadata(item_path),
                }

                if file_info['name'] in duplicates:
                    duplicates[file_info['name']].append(item_relative_path)
                    current_file_mtime = os.path.getmtime(item_path)
                    parent_file_mtime = os.path.getmtime(
                        duplicates[file_info['name']][-1])

                    if current_file_mtime > parent_file_mtime:
                        duplicates[file_info['name']][-1], duplicates[file_info['name']
                                                                      ][-2] = duplicates[file_info['name']][-2], duplicates[file_info['name']][-1]

                else:
                    duplicates[file_info['name']] = [item_relative_path]

                if item_relative_path != duplicates[file_info['name']][-1]:
                    continue

                tree['files'].append(file_info)

    else:
        print("Error: The provided path is not a folder!")

    tree['duplicates'] = duplicates
    return tree
