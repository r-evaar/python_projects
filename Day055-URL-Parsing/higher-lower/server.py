from flask import Flask, redirect, url_for, render_template
from utils import cmd
from styles import style

app = Flask(__name__)

@app.route('/')
def _():
    return redirect(url_for('home'))

@app.route('/home')
def home():
    return render_template('index.html', css='default')

if __name__ == '__main__':
    cmd(f'set FLASK_APP={__name__}')
    app.run(debug=True)
