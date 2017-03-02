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
