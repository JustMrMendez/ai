import os
import random
import string


def generate_random_folder_tree(root_dir, num_folders=15, max_depth=4, max_files=5):
    """
    Generates a random folder tree with files and some content in them.

    Args:
    - root_dir: The root directory of the folder tree.
    - num_folders: The number of folders to create.
    - max_depth: The maximum depth of the folder tree.
    - max_files: The maximum number of files to create in each folder.

    Returns:
    - None
    """
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)

    def create_folder(folder_path, depth):
        if depth >= max_depth:
            return
        for k in range(random.randint(1, max_files)):
            file_name = ''.join(random.choices(string.ascii_lowercase, k=8))
            file_path = os.path.join(folder_path, file_name + '.txt')
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    content = ''.join(random.choices(
                        string.ascii_lowercase, k=50))
                    f.write(content)
            else:
                with open(file_path, 'r') as f:
                    content = f.read()
            if random.random() < 0.5:
                # create a new sub-folder with the same name as an existing folder
                sub_folder_name = random.choice(folder_names)
                sub_folder_path = os.path.join(folder_path, sub_folder_name)
                if not os.path.exists(sub_folder_path):
                    os.makedirs(sub_folder_path)
                create_folder(sub_folder_path, depth + 1)
            if random.random() < 0.5:
                # create a new sub-folder
                sub_folder_name = ''.join(
                    random.choices(string.ascii_lowercase, k=8))
                sub_folder_path = os.path.join(folder_path, sub_folder_name)
                if not os.path.exists(sub_folder_path):
                    os.makedirs(sub_folder_path)
                create_folder(sub_folder_path, depth + 1)

    folder_names = []
    for i in range(num_folders):
        folder_name = ''.join(random.choices(string.ascii_lowercase, k=8))
        if folder_name in folder_names:
            folder_name += f"_{random.randint(1000, 9999)}"
        folder_path = os.path.join(root_dir, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        folder_names.append(folder_name)
        create_folder(folder_path, 1)
