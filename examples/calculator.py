import sys
import operator
import streams


def add(out, channel1, channel2):
    while True:
        op1, op2 = channel1.take(), channel2.take()
        sys.stdout.write('Calculating ({} + {})'.format(op1, op2))
        res = operator.add(op1, op2)
        out.give(res)


def mul(out, channel1, channel2):
    while True:
        op1, op2 = channel1.take(), channel2.take()
        sys.stdout.write(' * {}\n'.format(op2))
        res = operator.mul(op1, op2)
        out.give(res)


if __name__ == '__main__':
    input_channel1, input_channel2, input_channel3 = \
        streams.InputChannel(iter(xrange(5)), 'c1'), \
        streams.InputChannel(iter(xrange(0, 10, 2)), 'c2'), \
        streams.InputChannel(iter(xrange(1, 6)), 'c3')

    flow = streams.ExecutionFlow()
    add_switch = flow.new_bolt(add, 'add', input_channel1, input_channel2)
    mul_switch = flow.new_bolt(mul, 'mul', add_switch.out_channel,
                               input_channel3)
    while True:
        try:
            res = flow.run()
            print('result: {}'.format(res))
        except StopIteration:
            print('Finished processing')
            break
