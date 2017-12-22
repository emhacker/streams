'''
Example: Eratosthenes sieve
(https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes)
Implemented in streams. (The sieve identifies numbers <= 10).
'''
import streams


def prime2(out, channel):
    while True:
        num = channel.take()
        if num <= 1:
            continue
        if num == 2 or num % 2:
            out.give(num)


def prime3(out, channel):
    while True:
        num = channel.take()
        if num == 3:
            out.give(3)
            continue
        if num % 3:
            out.give(num)
            continue
        if num >= 9:
            # EOF.
            out.give(None)


if __name__ == '__main__':
    channel = streams.InputChannel(iter(xrange(10)), 'c1')
    flow = streams.ExecutionFlow()
    b2 = flow.new_bolt(prime2, 'prime2', channel)
    flow.new_bolt(prime3, 'prime3', b2.out_channel)
    while True:
        try:
            p = flow.run()
            if p:
                print('{} is a prime number.'.format(p))
        except StopIteration:
            print('All finished.')
            break
