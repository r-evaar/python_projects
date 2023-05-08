import subprocess

def css(filename):
    with open(f'static/css/{filename}.css', 'r') as f:
        return f.read()

def cmd(command):
    subprocess.run(['cmd', '/c', command], stdout=subprocess.PIPE)
