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
# Record data script path.
RECORD_USAGE = os.path.join(PROJ_PATH, 'app/record_usage.py')
# Data storage directory path.
STORE_PATH = os.path.join(PROJ_PATH, 'temp')
if not os.path.exists(STORE_PATH):
    os.makedirs(STORE_PATH)

# Storage file path.
STORE_FILE = os.path.join(STORE_PATH, 'store')

# Sampling frequency to track cpu usage.
SAMPLING_FREQ = 1  # in seconds.
# Time interval over which average is calculated.
AVG_INTERVAL = 60  # in seconds.

# Host for which the web server is to be run.
HOST = 'localhost'
# Port number the web server should listen to.
PORT = 8845

# Messages for web server.
START_MSG = 'Started HTTP Server, use <Ctrl-C> to stop ...'
STOP_MSG = 'Stopping HTTP Server...'
UNKNOWN_REQ = 'Unknown request.'

# URLs.
STATS = '/stats'
USAGE = '/cpu_usage'
