from greenlet import greenlet


class Channel(object):
    '''
    A data channel conveying data from a Bolt.
    '''
    def __init__(self):
        self.g = greenlet.getcurrent()

    def give(self, v):
        self.v = v
        self.g.switch()

    def take(self):
        return self.v


class InputChannel(object):
    '''
    Data channel conveying data from an out-of-process data source.
    '''
    def __init__(self, src, name):
        self.src = src
        self.name = name

    def take(self):
        ret = next(self.src)
        return ret

    def give(self, v):
        raise Exception('Operation not supported')


class Bolt(object):
    def __init__(self, op, name, *input_channels):
        self.g = greenlet(op)
        self.name = name
        self.out_channel = Channel()
        self.input_channels = input_channels

    def switch(self):
        if not self.g:
            self.g.switch(self.out_channel, *self.input_channels)
        else:
            self.g.switch()
        return self.out_channel.take()


WHITE, GRAY, BLACK = 0, 1, 2


class ExecutionFlow:

    class Node:
        def __init__(self, b):
            self.b = b
            self.color = WHITE

        def reach(self, all_nodes):
            for n in all_nodes:
                if self == n:
                    continue
                if self.b.out_channel in n.b.input_channels:
                    yield n

    def __init__(self):
        self.nodes = list()
        self.ordered = list()

    def new_bolt(self, op, name, *input_channels):
        bolt = Bolt(op, name, *input_channels)
        self.nodes.append(ExecutionFlow.Node(bolt))
        return bolt

    def _top_sort(self):

        def _visit(cur, ordered):
            if cur.color == BLACK:
                return
            if cur.color == GRAY:
                raise Exception('Cycle detected in execution graph')
            cur.color = GRAY
            for n in cur.reach(self.nodes):
                _visit(n, ordered)
            cur.color = BLACK
            ordered.append(cur)

        ordered = list()
        for cur in self.nodes:
            if cur.color != WHITE:
                continue
            _visit(cur, ordered)
        return [n.b for n in reversed(ordered)]

    def run(self):
        if not self.ordered:
            self.ordered = self._top_sort()
        for bolt in self.ordered:
            res = bolt.switch()
        return res
