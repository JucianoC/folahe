import os
from fabric.api import run, env, local, hosts


def tests():
    commands = [
        'PYTHONPATH=./',
        'python -m pytest -v --cov-report term-missing --cov=. tests/'
        ' --showlocals --pep8',
    ]
    local(';'.join(commands))
