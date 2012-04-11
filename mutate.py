# various different mutation operations on stack programs
from functools import partial
from itertools import chain, islice

# deleter - removes a section of a program
# repeater - repeats some words in a program
# reverser - reverses a section
# inserter - inserts a randomly selected item
# littletweaker - changes the value of an item (but leaves it the same kind of thing (by arity))
# bigtweaker - replaces an item with one of a different type (by arity)
# crosser - takes two and combines them together

class RangeMutator(object):

    def __init__(self, seed):
        self.start = seed.next()
        val = seed.next()
        self.items = 0
        while True:
            self.items += 1
            val *= 2
            if val >= 1:
                break

    def __repr__(self):
        return '<{0.__class__.__name__} start={0.start} items={0.items!r}>'.format(self)

    def get_range(self, length):
        start = int(self.start * length)
        return start, start + self.items

    def mutate(self, sequence):
        return self._mutate_range(sequence, self.get_range(len(sequence)))

class Deleter(RangeMutator):
    def _mutate_range(self, sequence, (start, stop)):
        return list(chain(
            islice(sequence, None, start),
            islice(sequence, stop, None)))

class Repeater(RangeMutator):
    def _mutate_range(self, sequence, (start, stop)):
        return list(chain(
            islice(sequence, None, start),
            islice(sequence, start, stop),
            islice(sequence, start, stop),
            islice(sequence, stop, None)))

class Reverser(RangeMutator):
    def _mutate_range(self, sequence, (start, stop)):
        return list(chain(
            islice(sequence, None, start),
            reversed(sequence[start:stop]),
            islice(sequence, stop, None)))


# inserter needs to decide - where to insert, what to insert
# kinds of things - numbers, vars, funcs, operators

def pick_number(seed):
    val = seed.next()
    return str(int(val * val * 10000))

def pick_var(seed):
    return 't'

OPERATORS = '+ - * / >> & | ^ % !!'.split()

def pick_from_list(items, seed):
    return items[int(seed.next() * len(items))]

PICKERS = [
    (0.1, pick_var),
    (0.6, pick_number),
    (1.0, partial(pick_from_list, OPERATORS)),
]

class Inserter(object):

    def __init__(self, seed, pickers=None):
        pickers = pickers or PICKERS
        self.start = seed.next()
        threshold = seed.next()
        for value, picker in pickers:
            if value >= threshold:
                break
        self.item = picker(seed)

    def __repr__(self):
        return '<Inserter start={0.start} item={0.item!r}>'.format(self)

    def mutate(self, sequence):
        pos = int(self.start * len(sequence))
        return list(
            chain(
                islice(sequence, None, pos),
                [self.item],
                islice(sequence, pos, None)))
