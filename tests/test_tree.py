from unittest import TestCase

from ..tree import Node

class TreeTests(TestCase):

    def make_tree(self):
        a, b, c = Node('a'), Node('b'), Node('c')
        return Node('some text', children=[a, b, c])

    def test_last_child(self):
        root = self.make_tree()
        self.assertEqual(root.last_child.value, 'c')
        self.assertEqual(root.last_child.last_child, None)

    def test_parent(self):
        root = self.make_tree()
        c = root.last_child
        self.assertEqual(c.parent, root)
        self.assertEqual(root.parent, None)

    def test_left(self):
        root = self.make_tree()
        c = root.last_child
        b = c.left
        a = b.left
        self.assertEqual(b.value, 'b')
        self.assertEqual(a.value, 'a')
        self.assertEqual(a.left, c)
        self.assertEqual(root.left, None)

    def test_right(self):
        root = self.make_tree()
        c = root.last_child
        a = c.right
        b = a.right
        self.assertEqual(a.value, 'a')
        self.assertEqual(b.value, 'b')
        self.assertEqual(b.right, c)
        self.assertEqual(root.right, None)

    def test_add_child(self):
        root = self.make_tree()
        d = Node('d')
        root.add_child(d)
        self.assertEqual(root.last_child, d)
        self.assertEqual(d.parent, root)
