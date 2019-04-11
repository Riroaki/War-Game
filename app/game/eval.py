N = 10
TOP = 20

with open('./app/game/data.txt', 'r') as f:
    lines = f.readlines()
data = [line[:-1].split('\t') for line in lines]
data = [[int(i) for i in line] for line in data]

with open('./app/game/scores.txt', 'r') as f:
    line = f.read()
scores = [float(i) for i in line.split('\t')]


def compare(s1, s2):
    l, r = [], []
    for i in range(0, N):
        l.append(s1[i] * (i + 1) > s2[i])
        r.append(s2[i] * (i + 1) > s1[i])
    return l, r


def compete(s0, others=data):
    win = [0 for _ in range(10)]
    beaten = [0 for _ in range(10)]
    for s in others:
        l, r = compare(s0, s)
        win = [win[i] + l[i] for i in range(10)]
        beaten = [beaten[i] + r[i] for i in range(10)]
    win = [win[i]/1000 for i in range(10)]
    beaten = [beaten[i]/1000 for i in range(10)]
    rank = findRank(sum(win)*100)
    return [win, beaten], rank


def findRank(rate):
    for index in range(len(scores)):
        if rate > scores[index]:
            break
    return index


if __name__ == '__main__':
    compete(1)
