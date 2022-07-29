"""Make a filetree example.

Adapted from https://realpython.com/directory-tree-generator-python/

See the companion Jupyter notebook ../filetree_example.ipynb to see demos
on how to use this code.

"""

import os


class DirectoryTree:
    def __init__(self, filetree, use_pipe=True):
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

    def _tree_body(self, directory, prefix=""):
        """
        Loops through the dictionary content representing a directory
        and append the content to the tree.
        This is done recursively any time a new dictionary is encountered.
        """

        entries_count = len(directory)

        for index, entry in enumerate(directory):

            # change connector if this is the last item in this directory
            connector = self.ELBOW if index == entries_count - 1 else self.TEE
            self._add_dictionary(
                directory, entry, index, entries_count, prefix, connector
            )

    def _add_dictionary(
        self, directory, entry, index, entries_count, prefix, connector
    ):
        # We are dealing with a file
        if isinstance(directory[entry], str):
            self._add_file(entry, prefix, connector, directory[entry])
            return

        # We are dealing with a directory
        else:
            self._tree.append(f"{prefix}{connector} {entry}{os.sep}")
            prefix += (
                self.PIPE_PREFIX if index != entries_count - 1 else self.SPACE_PREFIX
            )
            self._tree_body(directory=directory[entry], prefix=prefix)

    def _add_file(self, entry, prefix, connector, comment=""):
        self._tree.append(f"{prefix}{connector} {entry} {comment}")
