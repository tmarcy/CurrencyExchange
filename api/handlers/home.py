from api import app
from flask import render_template


@app.route('/')
def homepage():
    handlers = [('new conversion', '/conversion'),
                ('most popular', '/api/v1.0/stats'),
                ('api_insert', '/api/v1.0/insert')
                ]

    return render_template('home.html', handlers=handlers)