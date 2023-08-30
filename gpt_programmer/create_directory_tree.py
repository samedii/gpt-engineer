import io
from contextlib import redirect_stdout
from pathlib import Path

from treelib import Tree


def create_directory_tree(directory_path, parent_node=None, tree=None):
    if tree is None:
        tree = Tree()
        tree.create_node(directory_path, directory_path)  # root node
        parent_node = directory_path

    directory = Path(directory_path)

    if not directory.is_dir():
        return "Provided path is not a directory."

    try:
        for entry in directory.iterdir():
            # skip __pycache__ directories
            if entry.name == "__pycache__":
                continue

            # read lines in gitignore
            gitignore = Path(".gitignore").read_text().splitlines()
            # skip entries in gitignore
            if entry.name in gitignore:
                continue

            node_identifier = str(entry)

            if entry.is_dir():
                tree.create_node(entry.name, node_identifier, parent=parent_node)
                create_directory_tree(node_identifier, node_identifier, tree)
            else:
                tree.create_node(entry.name, node_identifier, parent=parent_node)
    except PermissionError as e:
        print(f"PermissionError: {e}")

    return tree
