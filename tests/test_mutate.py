from unittest import TestCase

from ..mutate import Deleter, Repeater, Reverser

class TestMutators(TestCase):

    def test_deleter(self):
        d = Deleter(iter([0.5, 0.25]))
        # start is the fraction of the length to begin deleting at
        self.assertEqual(d.start, 0.5)
        # it'll delete items words, multiplying stop by 2 until it's >= one
        self.assertEqual(d.items, 2)
        self.assertEqual(d.get_range(10), (5, 7))
        d.start = 0.41
        d.items = 1
        self.assertEqual(d.get_range(10), (4, 5))
        self.assertEqual(d.get_range(5), (2, 3))
        prog = ['1', '2', '3', '4', '5']
        self.assertEqual(d.mutate(prog), ['1', '2', '4', '5'])

    def test_repeater(self):
        r = Repeater(iter([0.7, 0.125]))
        self.assertEqual(r.start, 0.7)
        self.assertEqual(r.items, 3)
        self.assertEqual(r.get_range(20), (14, 17))
        prog = list('0123456789')
        self.assertEqual(r.mutate(prog), list('0123456789789'))
        self.assertEqual(r.mutate(list('123')), list('1233'))

    def test_reverser(self):
        r = Reverser(iter([0.2, 0.23]))
        self.assertEqual(r.mutate(list('1234567')), list('1432567'))
