import logging
from logging.handlers import TimedRotatingFileHandler

from flask import Flask

app = Flask(__name__)


@app.route('/')
def foo():
    app.logger.warning('A warning occurred (%d apples)', 42)
    app.logger.error('An error occurred')
    app.logger.info('Info')
    return "foo"


if __name__ == '__main__':
    #handler = TimedRotatingFileHandler('D:/temp/foo.log')
    #handler.setLevel(logging.INFO)
    #app.logger.addHandler(handler)
    app.run()
