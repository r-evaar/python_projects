from flask import Flask
from datetime import datetime
from styler import *
import subprocess

app = Flask(__name__)

@app.route('/')
def hellow_world():
    return '<p>Hello, World!</p>'

@app.route('/username/<username>/default')
@style('default')
def greet(username):
    return f'''
<body>
    <p>Hi, {username}!</p>
    <h5>{datetime.now().strftime('%Y/%m/%d')}<h5>
</body>
'''

@app.route('/converters/path/<path:value>')
def conv_path(value):
    return f'<p>value = {value}</p>'

@app.route('/error-example/')
def error():
    return f'<p>value={intended_error}</p>'

def cmd(command):
    subprocess.run(['cmd', '/c', command], stdout=subprocess.PIPE)

if __name__ == '__main__':
    cmd(f'set FLASK_APP={__name__}')
    app.run(debug=True)
