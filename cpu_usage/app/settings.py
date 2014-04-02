'''Application settings file. Maintains user input config values.

@created: Mar 23, 2014
@author: Anshu Kumar, <anshu.choubey@imaginea.com>
'''
import os

# Project path.
PROJ_PATH = os.path.dirname(os.path.dirname(os.path.join(os.getcwd(),
                                                         __file__)))
# Static components path.
STATIC_PATH = os.path.join(PROJ_PATH, 'static')

# Sampling frequency to track cpu usage.
SAMPLING_FREQ = 1  # in seconds.
# Time interval over which average is calculated.
AVG_INTERVAL = 60  # in seconds.
# Decimal places to round to.
ROUND_TO = 2

# Host for which the web server is to be run.
HOST = 'localhost'
# Port number the web server should listen to.
PORT = 8845

# Messages for web server.
START_MSG = '\n'.join([
    'Started HTTP Server, use <Ctrl-C> to stop ...',
    'Please open the URL http://localhost:8845/stats in browser.',
    ])
STOP_MSG = 'Stopping HTTP Server...'
UNKNOWN_REQ = 'Unknown request.'

# URLs.
STATS = '/stats'
USAGE = '/cpu_usage'

# HTTP error codes.
HTTP_INTERNAL_SERVER_ERROR = 500
HTTP_NOT_FOUND = 404
HTTP_OK = 200
