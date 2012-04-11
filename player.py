#! /usr/bin/python
from argparse import ArgumentParser
import math
import re
import sys
from textwrap import dedent

pattern = 't 42 t 10 >> & *'

def _index(number, digit):
    chars = str(number)
    return int(chars[digit % len(chars)])

def make_generator(expr):
    body = dedent("""\
    def gen():
        sin = math.sin
        cos = math.cos
        tan = math.tan
        ceil = math.ceil
        index = _index
        t = (yield None)
        while True:
            t = yield ({0})
    """)
    _globals = dict(math=math, _index=_index)
    _locals = {}
    exec body.format(expr) in _globals, _locals
    func = _locals['gen']
    gen = func()
    gen.next()
    return gen.send

def _safe_pop(items):
    try:
        return items.pop()
    except IndexError:
        return '0'

NUMBERS = re.compile(r'^-?[0-9]+\.?[0-9]*$')
VARS = re.compile(r'^(t|pi)$')
FUNCS = re.compile(r'^[_a-zA-Z][_a-zA-Z0-9]*$')

ARITIES = [(NUMBERS, 0), (VARS, 0), (FUNCS, 1)]

def _arity(word):
    for _type, result in ARITIES:
        if _type.match(word):
            return result
    return 2

def _flatten(tree):
    if not isinstance(tree, list):
        return [tree]
    result = []
    for node in tree:
        if isinstance(node, list):
            result.extend(_flatten(node))
        else:
            result.append(node)
    return result

def _deparen(items):
    if items and items[0] == '(' and items[-1] == ')':
        return items[1:-1]
    return items

SPECIAL_OPERATORS = {
    '!!': 'index'
}

def to_infix(expr):
    stack = []
    words = expr.split()

    def add_binop(stack, word):
        op2 = _safe_pop(stack)
        op1 = _safe_pop(stack)
        special = SPECIAL_OPERATORS.get(word)
        if special:
            result = [special, '(', op1, ', ', op2, ')']
        else:
            result = ['(', op1, ' ', word, ' ', op2, ')']
        stack.append(result)

    for word in words:
        arity = _arity(word)
        if arity == 0:
            stack.append(word)
        elif arity == 1:
            operand = _safe_pop(stack)
            stack.append([word, '(',  _deparen(operand), ')'])
        else:
            add_binop(stack, word)
    while len(stack) > 1:
        add_binop(stack, '+')
    return ''.join(_flatten(_safe_pop(stack)))

class Sequencer(object):

    def __init__(self, program, start):
        self.t = start
        self._program = None
        self._g = None
        self.program = program

    def __iter__(self):
        return self

    def next(self):
        sample = int(self._g(self.t)) & 0xff
        result = self.t, sample
        self.t += 1
        return result

    @property
    def program(self):
        return self._program

    @program.setter
    def program(self, value):
        self._program = value
        self._g = make_generator(self._program)

def make_seq(pattern, start):
    g = make_generator(pattern)
    t = start
    while True:
        sample = int(g(t)) & 0xff
        yield t, sample
        t += 1


def main(pattern, start):
    _write = sys.stdout.write
    try:
        for t, sample in make_seq(pattern, start):
            _write(chr(sample))
    except KeyboardInterrupt:
        print >> sys.stderr, 'Last time:', t

parser = ArgumentParser(description='Run a bytebeat program.')
parser.add_argument('-s', '--start', metavar='T', type=int, default=0,
                    help='Start time value, defaults to 0.')
parser.add_argument('-i', '--infix', dest='postfix', action='store_false',
                    default=True,
                    help='Indicates program is in infix notation rather than superior postfix.')
parser.add_argument('program', help='Program code.', default=pattern)

if __name__ == '__main__':
    args = parser.parse_args()
    try:
        expr = args.program
        if args.postfix:
            expr = to_infix(expr)
            print >> sys.stderr, expr
        main(expr, args.start)
    except KeyboardInterrupt:
        sys.exit(0)
