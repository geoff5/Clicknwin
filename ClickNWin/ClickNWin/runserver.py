"""
This script runs the ClickNWin application using a development server.
"""

from os import environ
from ClickNWin import app

if __name__ == '__main__':
    #app.debug = False
    HOST = environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
