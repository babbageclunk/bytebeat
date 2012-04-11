from unittest import TestCase

from ..mutate import (
    Deleter, Inserter, Repeater, Reverser, pick_number, pick_var, pick_from_list
)

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

    def test_pick_number(self):
        self.assertEqual(pick_number(iter([0.2])), '400')

    def test_pick_var(self):
        self.assertEqual(pick_var(None), 't')

    def test_pick_from_list(self):
        vals = range(20)
        self.assertEqual(pick_from_list(vals, iter([0.21])), 4)

    def test_inserter(self):
        def make_picker(prefix):
            return lambda s: prefix + ' ' + str(s.next())
        fake_pickers = [(0.5, make_picker('p1')), (1.0, make_picker('p2'))]
        i = Inserter(iter([0.3, 0.25, 0.1]), pickers=fake_pickers)
        self.assertEqual(i.start, 0.3)
        self.assertEqual(i.item, 'p1 0.1')

        i = Inserter(iter([0.3, 0.75, 0.1]), pickers=fake_pickers)
        self.assertEqual(i.item, 'p2 0.1')

        self.assertEqual(i.mutate(list('01234')),
                         ['0', 'p2 0.1', '1', '2', '3', '4'])

    def test_reprs(self):
        self.assertEqual(repr(Deleter(iter([0.1, 0.1]))),
                         '<Deleter start=0.1 items=4>')
        self.assertEqual(repr(Reverser(iter([0.1, 0.1]))),
                         '<Reverser start=0.1 items=4>')
        self.assertEqual(repr(Repeater(iter([0.1, 0.1]))),
                         '<Repeater start=0.1 items=4>')
        fake_pickers = [(1.0, lambda _: 'item')]
        self.assertEqual(repr(Inserter(iter([0.1, 0.1]), pickers=fake_pickers)),
                         '<Inserter start=0.1 item=\'item\'>')
