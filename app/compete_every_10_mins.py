from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
import os

# 实例化一个调度器
scheduler = BlockingScheduler()
START = -1
END = 25
seprator = '!'


def compare(s1, s2):
    l, r = [], []
    for i in range(0, 10):
        l.append(s1[i] * (i + 1) > s2[i])
        r.append(s2[i] * (i + 1) > s1[i])
    return l, r


def extract_best():
    hour = datetime.datetime.now().hour
    minute = datetime.datetime.now().minute
    if hour < START or hour > END:
        return

    # Get strategies from files.
    round = minute // 10 + 1
    posts = {}
    times = {}
    path = './data/competitionData/'
    fileList = [file for file in os.listdir(path) if file.endswith('.txt')]
    # numberOfCompetitors = len(fileList)
    for filename in fileList:
        user_id = filename[:filename.find('.txt')]
        with open(path + filename, 'r') as f:
            temp = f.readlines()[-1]
            if temp.endswith('\n'):
                continue
            temp = temp.split(seprator)
            strategy = [int(i) for i in temp[1].split(',')]
            times[user_id] = temp[2]
            if int(temp[0]) != round:
                # continue
                pass
            posts[user_id] = strategy
    numberOfCompetitors = len(posts)

    # Get the results and rank for each strategy.
    allResults = {}
    for k1, v1 in posts.items():
        allResults[k1] = [0 for _ in range(10)]
        for _, v2 in posts.items():
            l, _ = compare(v1, v2)
            allResults[k1] = [allResults[k1][i] + l[i] for i in range(10)]
        allResults[k1] = [i / numberOfCompetitors for i in allResults[k1]]
    allScores = [(k, sum(v)) for k, v in allResults.items()]
    sortedScores = sorted(allScores, key=lambda x: x[1], reverse=True)
    for rank, item in enumerate(sortedScores):
        user_id = item[0]
        result = [str(i) for i in allResults[user_id]]
        with open(path + user_id + '.txt', 'a') as f:
            f.write(','.join(result) + seprator + str(rank + 1) + '\n')

    # Write the best ones into best.txt.
    bests = 10
    if len(sortedScores) < bests:
        bests = len(sortedScores)
    current = str(datetime.datetime.now())
    with open('./data/best.txt', 'a') as f:
        f.write('current time:' + current + '\n')
        for i in range(bests):
            user_id = sortedScores[i][0]
            result = [str(j) for j in allResults[user_id]]
            f.write(
                str(i + 1) + seprator + user_id + seprator + ','.join(result) +
                seprator + times[user_id] + '\n')


# 添加任务并设置触发方式为3s一次
# scheduler.add_job(extract_best, 'interval', seconds=1000)

# 开始运行调度器
# scheduler.start()

if __name__ == '__main__':
    extract_best()
