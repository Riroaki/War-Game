from flask import render_template, request, redirect
from flask_login import current_user, logout_user, login_user
from app import app
from app import login_manager
from app.models import User
from app.game.eval import compete
from hashlib import md5
import datetime

START = -1
END = 25
seprator = '!'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# def login_required(func):
#     def wrapper(*args, **kw):
#         if current_user.is_authenticated:
#             return func(*args, **kw)
#         else:
#             return redirect('/login')
#     return wrapper


# The home page of the game.
@app.route('/war', methods=['GET'])
def index():
    user = current_user
    if len(current_user.__repr__()) > 30:
        user = 'Who am I?'
    return render_template("index.html", whoami=user, start=START, end=END)


# Login area.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if (request.method == 'GET'):
        if current_user:
            logout_user()
        return render_template('login.html')
    else:  # POST
        form = request.form
        user_id = form.get('user_id')
        pwd = form.get('pwd')
        user = User(user_id, pwd)

        # Encrypt the pwd.
        encrypter = md5()
        encrypter.update(pwd.encode(encoding='utf-8'))
        pwd = encrypter.hexdigest()

        # Check both lower case and upper case.
        if user.query.filter_by(
                SID=user_id,
                PASSWORD=pwd.lower()).first() or user.query.filter_by(
                    SID=user_id, PASSWORD=pwd.upper()).first():
            login_user(user, remember=True)
            return redirect('/war')
        else:
            warning = '账号或密码不正确'
            return render_template('login.html', warning=warning)


# The practice area and the history of practice.
@app.route('/practice', methods=['POST', 'GET'])
# @login_required
def practice():
    if current_user.is_authenticated is None:
        return redirect('/login')
    return render_template('practice.html')


# History graph of current user.
@app.route('/practiceHistory', methods=['GET'])
# @login_required
def practiceHistory():
    if current_user.is_authenticated is None:
        return redirect('/login')
    try:
        with open(
                './app/data/practiceData/' + current_user.__repr__() + '.txt',
                'r') as f:
            history = f.readlines()
            history = [entry[:-1].split(seprator) for entry in history]
    except FileNotFoundError:
        history = ''
    return render_template('practiceHistory.html', history=history)


# The result area, generated for the practice area.
@app.route('/result', methods=['POST', 'GET'])
# @login_required
def result():
    if current_user.is_authenticated is None:
        return redirect('/login')
    strategy = ''
    result = ''
    rank = ''
    current = ''
    if request.method == 'POST':
        form = request.form
        strategy = [int(form.get("area" + str(i))) for i in range(1, 11)]
        if sum(strategy) != 100:
            strategy = ''
        else:
            current = str(datetime.datetime.now())
            result, rank = compete(strategy)

            # One entry represent one record of practice.
            entry = current + seprator + ','.join(
                [str(i) for i in strategy]) + seprator + ','.join(
                    [str(i) for i in result[0]]) + seprator + str(rank)

            # write the entry into the practice file.
            with open(
                    './app/data/practiceData/' + current_user.__repr__() +
                    '.txt', 'a') as f:
                f.write(entry + '\n')
    return render_template(
        'result.html',
        strategy=strategy,
        result=result,
        rank=rank,
        time=current)


# The compete area and the compete history.
@app.route('/compete', methods=['GET', 'POST'])
# @login_required
def real():
    if current_user.is_authenticated is None:
        return redirect('/login')
    if request.method == 'GET':
        hour = datetime.datetime.now().hour
        minite = datetime.datetime.now().minute
        second = datetime.datetime.now().second
        if hour < START or hour > END:  # Should be changed to 19 and 20
            return redirect('/war')
        else:
            return render_template(
                'compete.html',
                round=minite // 10 + 1,
                timeLeft=60 * (10 - minite % 10) - second,
                whoami=current_user)
    else:  # POST
        hour = datetime.datetime.now().hour
        minute = datetime.datetime.now().minute
        # Block invalid POSTS.
        if hour < START or hour > END:
            return redirect('/war')
        form = request.form
        strategy = [int(form.get("area" + str(i))) for i in range(1, 11)]
        if sum(strategy) != 100:
            strategy = ''
        else:
            current = str(datetime.datetime.now())
            round = minute // 10 + 1
        filename = './app/data/competitionData/' + current_user.__repr__(
        ) + '.txt'
        with open(filename, 'a') as f:
            # If read from f, the contents will be ''
            # because f points to the end of file.
            temp = open(filename, 'r')
            if temp.read().endswith(seprator):
                f.write('ignore\n')
            else:
                f.write(
                    str(round) + seprator +
                    ','.join([str(i) for i in strategy]) + seprator + current +
                    seprator)
            temp.close()
        return redirect('/war')


@app.route('/competeHistory', methods=['GET'])
# @login_required
def competeHistory():
    if current_user.is_authenticated is None:
        return redirect('/login')
    try:
        with open(
                './app/data/competitionData/' + current_user.__repr__() +
                '.txt', 'r') as f:
            lines = f.readlines()
            lines = [line for line in lines if not line.endswith(seprator)]
            lines = [line for line in lines if not line.endswith('ignore\n')]
            history = [entry[:-1].split(seprator) for entry in lines]
            print(history)
    except FileNotFoundError:
        history = ''
    except IndexError:
        print('index error in competition data!')
        history = ''
    return render_template('competeHistory.html', history=history)


@app.route('/ranks', methods=['GET'])
# @login_required
def ranks():
    if current_user.is_authenticated is None:
        return redirect('/login')
    with open('./app/data/best.txt', 'r') as f:
        content = f.read()
    index = content.rfind('current time:')
    if index == -1:
        best = ''
    else:
        lines = content[index:].split('\n')
        best = [line.split(seprator) for line in lines[1:-1]]
    return render_template('ranks.html', best=best)


# About the game...
@app.route('/instruct', methods=['GET'])
def instruct():
    return render_template('instruct.html')
