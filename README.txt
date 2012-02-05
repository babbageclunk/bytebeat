This is a small program that takes an expression and uses it to
generate bytes that you can pipe to aplay (or something else that will
interpret the bytes as sound).

Run it like so:

./player.py 'program goes here' | aplay

The idea is discussed at http://canonical.org/~kragen/bytebeat/

Originally it took a normal infix Python expression (using t to
represent time). That's still available using -i, but by default it
uses a postfix notation now. I switched because I'm thinking about
using genetic algorithms to find interesting music programs, and a
postfix notation lends itself better to mutating because there are no
syntax errors with mismatched brackets.

For the same reason, the postfix notation adds zeros at the bottom
of the stack to prevent stack underflows, and plus operators on the
right if there is more than one item left on the stack after
converting it to infix. So "1 2 + -" becomes "0 1 2 + -",  or "(0 - (1
+ 2))" in infix, and "1 2 + 3" becomes "1 2 + 3 +", which is "((1 + 2)
+ 3)".

I've also added an index operator (!!, stolen from Haskell) to match
some of the programs I saw online that got interesting patterns by
indexing into char arrays, like "2345"[t >> 10]. !! takes a number and
an index, and returns the digit at that index (modulo the length of
the number, to prevent errors). It gets converted into index(number,
idx) in infix notation. (I did that rather than just using Python's []
operation because using types other than numbers would make it
trickier to mutate the programs and still guarantee valid output.)
