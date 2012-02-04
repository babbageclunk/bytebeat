from math import cos, pi, sin, tan
from unittest import TestCase

from ..player import (
    _arity, _deparen, _flatten, _index, make_generator, _safe_pop, to_infix
)

class TestPlayer(TestCase):
    def test_make_generator(self):
        g = make_generator('t')
        self.assertEqual(g(4), 4)
        g = make_generator('t * t')
        self.assertEqual(g(10), 100)
        g = make_generator('sin(t) + cos(t) + tan(t) + ceil(t)')
        expected = sin(pi / 2) + cos(pi / 2) + tan(pi / 2) + 2
        self.assertEqual(g(pi / 2), expected)

    def test_to_infix(self):
        self.assertEqual(to_infix(''), '0')
        self.assertEqual(to_infix('t 3 +'), '(t + 3)')
        self.assertEqual(to_infix('4 t 3 +'), '(4 + (t + 3))')
        self.assertEqual(to_infix('4 t'), '(4 + t)')
        self.assertEqual(to_infix('3 +'), '(0 + 3)')
        self.assertEqual(to_infix('+'), '(0 + 0)')
        self.assertEqual(to_infix('+ *'), '(0 * (0 + 0))')
        self.assertEqual(to_infix('t 3 &'), '(t & 3)')
        self.assertEqual(to_infix('t 3 4'), '(t + (3 + 4))')
        self.assertEqual(to_infix('t sin'), 'sin(t)')
        self.assertEqual(to_infix('t cos'), 'cos(t)')
        self.assertEqual(to_infix('t tan'), 'tan(t)')
        self.assertEqual(to_infix('t blamp'), 'blamp(t)')
        self.assertEqual(to_infix('ceil'), 'ceil(0)')
        self.assertEqual(to_infix('t 3 + sin'), 'sin(t + 3)')
        self.assertEqual(to_infix('t 3 >>'), '(t >> 3)')
        self.assertEqual(to_infix('t 42 t 10 >> & *'), '(t * (42 & (t >> 10)))')

    def test_to_infix_with_index(self):
        self.assertEqual(to_infix('t 3 !!'), 'index(t, 3)')

    def test_index(self):
        self.assertEqual(_index(1234, 0), 1)
        self.assertEqual(_index(1234, 1), 2)
        self.assertEqual(_index(1234, 2), 3)
        self.assertEqual(_index(1234, 3), 4)
        self.assertEqual(_index(1234, -1), 4)
        self.assertEqual(_index(1234, 4), 1)
        self.assertEqual(_index(1234, 5), 2)

    def test_index_available_to_generator(self):
        g = make_generator('index(t, 1)')
        self.assertEqual(g(1234), 2)

    def test_safe_pop(self):
        self.assertEqual(_safe_pop([]), '0')
        l = ['1']
        self.assertEqual(_safe_pop(l), '1')
        self.assertEqual(l, [])

    def test_arity(self):
        self.assertEqual(_arity('3'), 0)
        self.assertEqual(_arity('3383'), 0)
        self.assertEqual(_arity('-3383'), 0)
        self.assertEqual(_arity('3383.93983'), 0)
        self.assertEqual(_arity('t'), 0)
        self.assertEqual(_arity('pi'), 0)
        self.assertEqual(_arity('sin'), 1)
        self.assertEqual(_arity('_flibberty9Gibbet'), 1)
        self.assertEqual(_arity('+'), 2)
        self.assertEqual(_arity('>>'), 2)
        self.assertEqual(_arity('&'), 2)
        self.assertEqual(_arity('!!'), 2)
        self.assertEqual(_arity('*****'), 2)

    def test_flatten(self):
        self.assertEqual(_flatten(['1']), ['1'])
        self.assertEqual(_flatten(['1', '2']), ['1', '2'])
        self.assertEqual(_flatten(['a', ['b'], 'c']), ['a', 'b', 'c'])

    def test_deparen(self):
        self.assertEqual(_deparen([]), [])
        self.assertEqual(_deparen(['whatever']), ['whatever'])
        self.assertEqual(_deparen(['(', 'thing', ')']), ['thing'])
        self.assertEqual(_deparen(['a', '(', 'thing', ')', 'b']),
                         ['a', '(', 'thing', ')', 'b'])
