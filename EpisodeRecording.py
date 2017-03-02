# https://www.hackerrank.com/challenges/episode-recording

from collections import defaultdict


def make_dict():
    return defaultdict(make_dict)


def ddict2dict(d):
    for k, v in d.items():
        if isinstance(v, dict):
            d[k] = ddict2dict(v)
    return dict(d)


s = defaultdict(make_dict)

seasons = int(input())

for i in range(seasons):
    episodes = int(input())
    for j in range(episodes):
        ar = input()
        ar = ar.split(' ')
        s[i][j]['live']['start'] = int(ar[0])
        s[i][j]['live']['end'] = int(ar[1])
        s[i][j]['repeat']['start'] = int(ar[2])
        s[i][j]['repeat']['end'] = int(ar[3])

s = ddict2dict(s)

class Tree(object):
    def __init__(self):
        self.live = None
        self.repeat = None
        self.data = None


def isInRange(ep, rng):
    i = 0
    while i<len(rng) and ep['start'] <= rng[i]['end']:
        i += 1

    if i >= len(rng) or ep['end'] < rng[i]['start']:
        return True

    return False

def getMaxInterval(root, i, j, length, rng=None):
    if j < length:
        if rng is None:

            rngl = []
            rngr = []
            root.live = Tree()
            rngl.append(s[i][j]['live'])
            root.live.data = getMaxInterval(root.live, i, j+1, length, rngl)

            root.repeat = Tree()
            rngr.append(s[i][j]['repeat'])
            root.repeat.data = getMaxInterval(root.repeat, i, j+1, length, rngr)

            ll = len(root.live.data)
            rl = len(root.repeat.data)

            if ll > rl:
                return root.live.data
            return root.repeat.data
        else:
            # recursiveness
            bl = isInRange(s[i][j]['live'], rng)
            br = isInRange(s[i][j]['repeat'], rng)
            if bl and br:
                root.live = Tree()
                rngl = list(rng)
                rngl.append(s[i][j]['live'])
                root.live.data = getMaxInterval(root.live, i, j+1, length, rngl)

                root.repeat = Tree()
                rngr = list(rng)
                rngr.append(s[i][j]['repeat'])
                root.repeat.data = getMaxInterval(root.repeat, i, j+1, length, rngr)

                ll = len(root.live.data)
                rl = len(root.repeat.data)

                if ll > rl:
                    return root.live.data
                return root.repeat.data

            elif bl:
                root.live = Tree()
                rng.append(s[i][j]['live'])
                sorted(rng, key=lambda epp: epp['start'])
                root.live.data = getMaxInterval(root.live, i, j+1, length, rng)

                return root.live.data
            elif br:
                root.repeat = Tree()
                rng.append(s[i][j]['repeat'])
                sorted(rng, key=lambda epp: epp['start'])
                root.repeat.data = getMaxInterval(root.repeat, i, j+1, length, rng)

                return root.repeat.data

            return rng
    return rng


def findR(i, j, length, st=None):
    if st is None:
        end = min(s[i][j]['live']['end'], s[i][j]['repeat']['end'])
        return findR(i, j + 1, length, end)
    else:
        if j >= length:
            return j
        else:
            startl = s[i][j]['live']['start']
            startr = s[i][j]['repeat']['start']

            if max(startl, startr) > st:

                if min(startl, startr) > st:
                    end = min(s[i][j]['live']['end'], s[i][j]['repeat']['end'])
                elif startl > st:
                    end = s[i][j]['live']['end']
                else:
                    end = s[i][j]['repeat']['end']

                return findR(i, j + 1, length, end)

            else:

                return j


diffs = []

for i in range(len(s)):
    for j in range(len(s[i])):
        root = Tree()

        rng = getMaxInterval(root, i, j, len(s[i]))

        diffs.append(len(rng)-1)

    m = max(diffs)
    print('diffs')
    print(diffs)
    x = diffs.index(m)
    print(x)

    print('{x} {y}'.format(x=x + 1, y=x +1+ m))
    diffs = []
