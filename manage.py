#!/usr/bin/env python

from flask.ext.script import Manager

from concurso import app


manager = Manager(app)


@manager.command
def hello():
    print "hello"


if __name__ == "__main__":
    manager.run()