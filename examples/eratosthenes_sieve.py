'''
Example: Eratosthenes sieve (https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes)
Implemented in streams. (The sieve identifies numbers <= 9).
'''
from greenlet import greenlet
import streams


def prime2(num):
    return num if num and num % 2 else None


def prime3(num):
    return num if num and num % 3 else None


def announce(n):
    print '{} is a prime number'.format(n)


if __name__ == '__main__':
    b2 = streams.Bolt(prime2, 'b2')
    b3 = streams.Bolt(prime3, 'b3')
    c = streams.Consumer(announce, 'C')
    # G2.
    b2.set_successors(b3)
    b3.set_successors(c)
    # G3.
    streams.dispatch(b2, xrange(6))
    print('All finished.')
