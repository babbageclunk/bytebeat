from itertools import imap, islice
from operator import itemgetter
from numpy import fromiter
import pygame
from random import choice, random
import sys

from mutate import Deleter, Inserter, Repeater, Reverser
from player import to_infix, Sequencer

generations = [
    't t 8 >> t 9 >> | * 46 & t 8 >> & t t 13 >> & t 6 >> | ^',
#    '2435687942743854 t 10 >>  !! t & 127 & t 9 >> t & 100 % 127 & -  2 -',
]

# Try to strike a balance between interactivity and not clicking on
# chunk boundaries.
CHUNKSIZE = 4000

# play through the population getting ratings for the user - rating
# corresponds to how many mutated descendants to generate.

pygame.mixer.pre_init(frequency=8000, size=8, channels=1)
pygame.init()
screen = pygame.display.set_mode((640, 480))

current = 0
seq = Sequencer(to_infix(generations[current]), 0)

def make_sound_chunk(seq, length):
    samples = fromiter(imap(itemgetter(1), islice(seq, length)), dtype='int8')
    return pygame.sndarray.make_sound(samples)

def play_and_queue(channel, seq):
    channel.play(make_sound_chunk(seq, CHUNKSIZE))
    channel.queue(make_sound_chunk(seq, CHUNKSIZE))

channel = pygame.mixer.find_channel()
channel.set_endevent(pygame.USEREVENT)
play_and_queue(channel, seq)

def change_current(direction):
    global current
    current += direction
    current = current % len(generations)
    print 'playing:', generations[current]
    seq.program = to_infix(generations[current])
    play_and_queue(channel, seq)

MUTATORS = [Inserter, Deleter, Repeater, Reverser]

def mutate(individual):
    mutator = choice(MUTATORS)(iter(random, None))
    individual = individual.split()
    mutated = mutator.mutate(individual)
    return mutator, ' '.join(mutated)

def mutate_current():
    mutator, new_individual = mutate(generations[current])
    print 'applied', mutator
    print 'got:', new_individual
    generations[current + 1:] = [new_individual]
    change_current(1)

finished = False

while not finished:
    for event in pygame.event.get():
        if (event.type == pygame.QUIT
            or event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
            finished = True
            break
        elif event.type == pygame.USEREVENT:
            channel.queue(make_sound_chunk(seq, CHUNKSIZE))
        elif event.type == pygame.KEYUP:

            if event.key == pygame.K_f:
                change_current(1)
            elif event.key == pygame.K_b:
                change_current(-1)
            elif event.key == pygame.K_m:
                mutate_current()
