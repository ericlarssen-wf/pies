from __future__ import absolute_import
import logging

from flask import Flask
import app_intelligence
import pyformance

app = Flask(__name__)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logsHandler = app_intelligence.logger.Handler()
logger.addHandler(logsHandler)

reporter = app_intelligence.telemetry.Reporter(
    pyformance.global_registry(),
    reporting_interval=5
)
reporter.set_toplevel_metadata(serverInfo='pies')
reporter.start()


@app.route('/')
def home():
    meta = app_intelligence.metadata(hello='world')
    context = app_intelligence.context(user_id='abc')

    pyformance.counter('homepage.hits').inc()

    with meta, context:
        logging.info('hello')

    logging.info('sharks', extra={'some':'metadata', 'account_id': 'abcdefg'})

    return '''
        <h1>Let's Make Some Logs</h1>
        <ul>
            <li><a href="/debug">Make debug log</a></li>
            <li><a href="/info">Make info log</a></li>
            <li><a href="/warning">Make warning log</a></li>
            <li><a href="/error">Make error log</a></li>
            <li><a href="/critical">Make critical log</a></li>
            <li><a href="/exception">Make exception log</a></li>
        </ul>
    '''

@app.route('/debug')
@pyformance.time_calls
def debug():
    logging.debug('this is debug')
    return 'You made a debug log!'


@app.route('/info')
@pyformance.time_calls
def info():
    logging.info('this is info')
    return 'You made an info log!'


@app.route('/warning')
@pyformance.time_calls
def warning():
    logging.warning('this is warning')
    return 'You made a warning log!'


@app.route('/error')
@pyformance.time_calls
def error():
    logging.error('this is error')
    return 'You made an error log!'


@app.route('/critical')
@pyformance.time_calls
def critical():
    logging.critical('this is critical')
    return 'You made a critical log!'


@app.route('/exception')
@pyformance.time_calls
def exception():
    try:
        x = 1/0
    except:
        logging.exception('Why did you think dividing by zero was a good idea?')
    return 'You made an exception log!'

app.wsgi_app = app_intelligence.WSGIMiddleware(app.wsgi_app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
