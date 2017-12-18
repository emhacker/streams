from greenlet import greenlet


def invoke_bolt(bolt, *args, **kwargs):
    g = greenlet(bolt)
    bolt.set_parent(g)
    g.switch(*args, **kwargs)


class Bolt(object):
    def __init__(self, f, name):
        self.f = f
        self.successors = []
        self.name = name

    def set_successors(self, *successors):
        self.successors = successors

    def set_parent(self, parent):
        self.parent = parent

    def __call__(self, *args, **kwargs):
        res = self.f(*args, **kwargs)
        if res is None:
            return
        for s in self.successors:
            invoke_bolt(s, *args, **kwargs)
        self.parent.switch()


class Consumer(object):
    def __init__(self, f, name):
        self.f = f
        self.name = name

    def __call__(self, *args, **kwargs):
        self.f(*args, **kwargs)

    def set_parent(self, _):
        pass


def dispatch(bolt, r):
    def _loop():
        for n in r:
            invoke_bolt(bolt, n)
    gdispatch = greenlet(_loop)
    gdispatch.switch()
