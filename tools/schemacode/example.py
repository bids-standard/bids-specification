"""Make a filetree example.

Adapated from by https://realpython.com/directory-tree-generator-python/

"""

import os

class DirectoryTree:
    def __init__(self, filetree):
        self._generator = _TreeGenerator(filetree)

    def generate(self):
        tree = self._generator.build_tree()
        text = "\n```Text\n"
        for entry in tree:
            text += entry
            text += "\n"
        text += "```\n"
        return text


class _TreeGenerator:
    def __init__(self, filetree):
        self._filetree = filetree
        self._tree = []
        self.PIPE = "│"
        self.ELBOW = "└──"
        self.TEE = "├──"
        self.PIPE_PREFIX = "│   "
        self.SPACE_PREFIX = "    "

    def build_tree(self):
        self._tree_body(self._filetree)
        return self._tree  

    def _add_directory(self, directory, entry, index, entries_count, prefix, connector):
        self._tree.append(f"{prefix}{connector} {entry}{os.sep}")
        prefix += self.PIPE_PREFIX if index != entries_count - 1 else self.SPACE_PREFIX
        self._tree_body(directory=directory[entry], prefix=prefix)
        self._tree.append(prefix.rstrip())

    def _add_file(self, entry, prefix, connector):
        self._tree.append(f"{prefix}{connector} {entry}")

    def _tree_body(self, directory, prefix=""):

        entries = self._preprare_entries_list(directory)
        entries_count = len(entries)

        for index, entry in enumerate(entries):

            connector = self.ELBOW if index == entries_count - 1 else self.TEE

            if isinstance(directory, dict):
                self._add_directory(
                    directory, entry, index, entries_count, prefix, connector
                )
            else:
                self._add_file(entry, prefix, connector)

    def _preprare_entries_list(self, directory):
        entries = directory
        return entries

def make_filetree_example(filetree_info):
    tree = DirectoryTree(filetree_info)
    return tree.generate()