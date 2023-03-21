from lib.testing import generate_random_folder_tree
from lib.pyvisTree import visualize_tree
from lib.tree import generate_tree
import os
import platform
import subprocess

# generate_random_folder_tree('test_folder')

tree = generate_tree('test_folder')

visualize_tree(tree)

# get current workinf d