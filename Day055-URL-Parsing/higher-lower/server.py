from flask import Flask, redirect, url_for, render_template
from utils import cmd
from random import randint

app = Flask(__name__)
gen = 0

style = 'default'

@app.route('/')
def _():
    return redirect(url_for('home'))

@app.route('/home', methods=['GET', 'POST'])
def home():
    global gen
    gen = randint(0, 9)
    print(f"New number generated: {gen}")
    prompt = 'Guess a number between 0 and 9'
    return render_template('index.html', css=style, img='num', txt=prompt, num='')

@app.route('/home/<string:num>', methods=['GET', 'POST'])
def guess(num):
    global gen
    num = int(num)
    if num > gen:
        img = 'high'
        txt = 'too high!'
    elif num < gen:
        img = 'low'
        txt = 'too low!'
    else:
        img = 'bingo'
        txt = 'correct!'

    return render_template('index.html', css=style, img=img, txt=txt, num=f'{num} is ')

if __name__ == '__main__':
    cmd(f'set FLASK_APP={__name__}')
    app.run(debug=True)
