def compare(s1, s2):
    l, r = [], []
    for i in range(0, 10):
        l.append(s1[i] * (i + 1) > s2[i])
        r.append(s2[i] * (i + 1) > s1[i])
    return l, r


with open('./data.txt', 'r') as f:
    lines = f.readlines()
data = [line[:-1].split('\t') for line in lines]
data = [[int(i) for i in line] for line in data]

rate = [0 for _ in range(len(data))]
for index1, s1 in enumerate(data):
    win = [0 for _ in range(10)]
    for index2, s2 in enumerate(data):
        if index1 == index2:
            continue
        l, _ = compare(s1, s2)
        win = [win[index] + l[index] for index in range(10)]
    rate[index1] = sum(win)/10
rate.sort(reverse=True)
with open('scores.txt', 'w') as f:
    f.write('\t'.join([str(i) for i in rate]))
