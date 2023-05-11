from flask import Flask, render_template
import subprocess

STYLER = 'default'

cmd = lambda c: subprocess.run(['cmd', '/c', c], stdout=subprocess.PIPE)

app = Flask(__name__, static_folder='./web', template_folder='./html')

@app.route('/')
def home(): return render_template('index.html', styler=STYLER)

if __name__ == '__main__':
    cmd(f'set FLASK_APP={__name__}')
    app.run(debug=True)
