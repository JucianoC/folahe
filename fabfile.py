import os
from fabric.api import run, env, local, hosts


def tests():
    commands = [
        'PYTHONPATH=./',
        'python -m pytest -v -x --cov-report term-missing --cov=. tests/'
        ' --showlocals --fulltrace --pep8',
    ]
    local(';'.join(commands))
