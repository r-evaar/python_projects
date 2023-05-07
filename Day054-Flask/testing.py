from flask import Flask
import subprocess

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Testing - 1</h1>"

if __name__ == "__main__":
    subprocess.run(['cmd', '/c', f'set FLASK_APP={__name__}'], stdout=subprocess.PIPE)
    app.run()
