import json
import time
import traceback

from flask import g
from flask import request

from . import create_app, db
from .routes import configure_routes

app = create_app()

configure_routes(app)

@app.before_request
def before_request():
    g.start = time.time()

@app.after_request
def after_request(response):
    diff = time.time() - g.start
    if ((response.response) and (200 <= response.status_code < 300)):
        app.logger.debug(f"Execution time: {diff}")
    return response

@app.errorhandler(Exception)
def exceptions(e):
    tb = traceback.format_exc()
    timestamp = time.strftime('[%Y-%b-%d %H:%M]')
    app.logger.error(
        '%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s',
        timestamp, request.remote_addr, request.method, request.scheme, request.full_path, tb
    )
    return e
