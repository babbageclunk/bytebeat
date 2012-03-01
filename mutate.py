# various different mutation operations on stack programs
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
