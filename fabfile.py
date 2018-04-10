import os
from fabric.api import run, env, local, hosts


def tests():
    local((
        'python -m pytest'
        '-v --cov-report term-missing --cov=. tests/ --pep8'))
