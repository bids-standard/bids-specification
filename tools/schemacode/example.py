"""Make a filetree example.

Adapated from by https://realpython.com/directory-tree-generator-python/

"""

import os


class DirectoryTree:
    def __init__(self, filetree, use_pipe = True):
        self._generator = _TreeGenerator(filetree, use_pipe)

    def generate(self):
        tree = self._generator.build_tree()
        text = "\n```Text\n"
        for entry in tree:
            text += entry
            text += "\n"
        text += "```\n"
        return text


class _TreeGenerator:
    def __init__(self, filetree, use_pipe):
        self._filetree = filetree
        self._tree = []
        self.PIPE = "│"
        self.ELBOW = "└─"
        self.TEE = "├─"
        self.PIPE_PREFIX = "│  "
        self.SPACE_PREFIX = "   "
        if not use_pipe:
            self.ELBOW = "  "
            self.PIPE = " "
            self.TEE = "  "
            self.PIPE_PREFIX = "   "

    def build_tree(self):
        self._tree_body(self._filetree)
        return self._tree

    def _add_dictionnary(
        self, directory, entry, index, entries_count, prefix, connector
    ):

        if isinstance(directory[entry], str):
            self._add_file(entry, prefix, connector, directory[entry])
            return

        else:  # We are dealing with a directory
            self._tree.append(f"{prefix}{connector} {entry}{os.sep}")
            prefix += (
                self.PIPE_PREFIX if index != entries_count - 1 else self.SPACE_PREFIX
            )
            self._tree_body(directory=directory[entry], prefix=prefix)

    def _add_file(self, entry, prefix, connector, comment=""):
        self._tree.append(f"{prefix}{connector} {entry} {comment}")

    def _tree_body(self, directory, prefix=""):

        entries_count = len(directory)

        for index, entry in enumerate(directory):

            connector = self.ELBOW if index == entries_count - 1 else self.TEE
            self._add_dictionnary(
                directory, entry, index, entries_count, prefix, connector
            )


def make_filetree_example(filetree_info, use_pipe):
    tree = DirectoryTree(filetree_info, use_pipe)
    return tree.generate()
