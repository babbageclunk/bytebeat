# Tree to let us navigate around the generations of programs.

class Node(object):

    def __init__(self, value, children=None):
        self.value = value
        self.parent = None
        self.index = None
        self.children = []
        children = children or []
        for child in children:
            self.add_child(child)

    def add_child(self, node):
        node.parent = self
        node.index = len(self.children)
        self.children.append(node)

    @property
    def last_child(self):
        if not self.children:
            return None
        return self.children[-1]

    def _get_sibling(self, direction):
        parent = self.parent
        if not parent:
            return None
        index = (self.index + direction) % len(parent.children)
        return parent.children[index]

    @property
    def left(self):
        return self._get_sibling(-1)

    @property
    def right(self):
        return self._get_sibling(1)
