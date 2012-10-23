from fabric.api import local

def build():
    local("python manage.py test teamhub")
    local("python setup.py sdist")