from itertools import imap, islice
from operator import itemgetter
from numpy import fromiter
from player import pattern, to_infix, make_seq
import pygame
import sys

pygame.mixer.pre_init(frequency=8000, size=8, channels=1)
pygame.init()

seq = make_seq(to_infix(pattern), 0)

def make_sound(seq, length):
    samples = fromiter(imap(itemgetter(1), islice(seq, length)), dtype='int8')
    return pygame.sndarray.make_sound(samples)

sound = make_sound(seq, 4000)
channel = pygame.mixer.find_channel()
channel.set_endevent(pygame.USEREVENT)
channel.play(sound)

next_sound = make_sound(seq, 4000)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.USEREVENT:
            print 'playing another one...'
            channel.play(next_sound)
            next_sound = make_sound(seq, 4000)
