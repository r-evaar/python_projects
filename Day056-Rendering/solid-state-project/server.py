from flask import Flask, render_template
from subprocess import run, PIPE

cmd = lambda c: run(['cmd', '/c', c], stdout=PIPE)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == "__main__":
    cmd(f'set FLASK_APP={__name__}')
    app.run(debug=True)
