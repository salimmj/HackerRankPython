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

    i=0
    while ep['start'] <= rng[i]['end']:
        i +=1

    if ep['end'] < rng[i+1]['start']:
        return True
    else:
        return False

def getMaxInterval(root, i, j, rng=None): #make root before calling
    if rng is None and j is None:

        root.live = Tree()
        rngl = rng.append(s[i][j]['live'])
        root.live.data = getMaxInterval(root.live, i, rng, j+1)

        root.repeat = Tree()
        rngr = rng.append(s[i][j]['repeat'])
        root.repeat.data = getMaxInterval(root.repeat, i, rng, j+1)

        return max(len(root.live), len(root.repeat))
    else:
        #recursiveness
        bl = isInRange(s[i][j]['live'], rng)
        br = isInRange(s[i][j]['repeat'], rng)
        if bl and br:
            root.live = Tree()
            rngl = list(rng)
            rngl.append(s[i][j]['live'])
            root.live.data = getMaxInterval(root.live, i, rngl, j+1)

            root.repeat = Tree()
            rngr = list(rng)
            rngr.append(s[i][j]['repeat'])
            root.repeat.data = getMaxInterval(root.repeat, i, rngr, j+1)

            return max(len(root.live.data), len(root.repeat.data))
        elif bl:
            root.live = Tree()
            rng.append(s[i][j]['live'])
            root.live.data = getMaxInterval(root.live, i, rng, j+1)
        elif br:
            rng.append(s[i][j]['repeat'])
            actualdata = getMaxInterval(i, repeat)
        else:
            return that episode


    #to sort sorted(student_tuples, key=lambda student: student[2])

def findR(i, j, length, st = None):
    if st is None:
        end = min(s[i][j]['live']['end'], s[i][j]['repeat']['end'])
        return findR(i, j+1, length, end)
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

                return findR(i, j+1, length, end)

            else:

                return j


LtoR = {}
diffs = []

for i in range(len(s)):
    for j in range(len(s[i])):

        LtoR[j] = findR(i, j, len(s[i]))

        diffs.append(LtoR[j] - j-1)

        if len(s[i])-j-1 <= max(diffs):
            break

    x = diffs.index(max(diffs))

    print('{x} {y}'.format(x=x+1, y=LtoR[x]))
    LtoR = {}
    diffs = []
