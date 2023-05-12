from flask import Flask, render_template
from subprocess import run, PIPE
from random import randint
from os import getlogin
from datetime import datetime as dt
from requests import get

cmd = lambda c: run(['cmd', '/c', c], stdout=PIPE)

app = Flask(__name__)

@app.route('/')
def home():
    kw = {
        'rand_num': f'{randint(1,100):03d}',
        'author': getlogin(),
        'year': dt.now().strftime('%Y')
    }
    return render_template('main.html', **kw)

def gender_and_age(name):
    response = get('https://api.genderize.io', params={'name': name})
    response.raise_for_status()
    gender = response.json()['gender']

    response = get('https://api.agify.io', params={'name': name})
    response.raise_for_status()
    age = response.json()['age']

    return gender, age

@app.route('/guess/<string:name>')
def guess(name):
    gender, age = gender_and_age(name)
    kw = {
        'name': name,
        'gender': gender,
        'age': age
    }
    return render_template('guessed.html', **kw)

@app.route('/test/<string:value>')
def test_json(value):
    return {'key': value}

@app.route('/blog')
def get_blog():
    r = get('https://api.npoint.io/5494f1118722971e2547')
    r.raise_for_status()
    return render_template('blog.html', posts=r.json())


if __name__ == '__main__':
    cmd(f'set FLASK_APP={__name__}')
    app.run(debug=True, host='0.0.0.0', port=5000)
