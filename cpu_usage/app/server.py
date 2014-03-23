'''Application web server.

@created: Mar 21, 2014
@author: Anshu Kumar, <anshu.choubey@imaginea.com>

@todo(Implement Logging)
'''

# pylint: disable=C0103

import json
import os
import sys

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from subprocess import Popen
from mimetypes import types_map

import record_usage as RU
import settings


class CPUUsageHandler(BaseHTTPRequestHandler):
    """Extended handler class for the web server."""

    def do_GET(self):
        """Over-ridden GET method."""
        self.path = self.path.rstrip('/')
        print "Path: ", self.path
        if self.path.endswith("favicon.ico"):
            return
        # Serve XHR.
        elif self.path.endswith(settings.USAGE):
            self.fetch_content(get_cpu_usage())
            return
        # Serve application request.
        elif self.path.endswith(settings.STATS):
            self.path = '/stats.html'
        _, ext = os.path.splitext(self.path)
        # Serve static components.
        if ext in (".html", ".css", '.js'):
            self.fetch_page(os.path.join(settings.STATIC_PATH,
                                         self.path.lstrip('/')), types_map[ext])
        else:
            # Unknown requests.
            self.send_error(501)

    def fetch_page(self, path, content_type='text/html', response=200):
        """Fetch response from a file to the client.

        Invokes fetch_content method after IO operation on the file.
        @param path: File path.
        @param content_type: Content type for the file. Defaults to text/html.
        @param response: Response code. Defaults to 200.
        @handles IOError: Send 404 error to the client.
        """
        try:
            with open(path) as fp:
                self.fetch_content(fp.read(), content_type, response)
        except IOError:
            self.send_error(404)

    def fetch_content(self, content, content_type='text/html', response=200):
        """Fetch response to the client.

        @param content: Content to be fetched.
        @param content_type: Type of the content. Defaults to text/html.
        @param response: Response code. Defaults to 200.
        """
        self.send_response(response)
        self.send_header('Content-type', content_type)
        self.end_headers()
        self.wfile.write(content)
        self.wfile.close()


def get_cpu_usage():
    """Returns the JSON format CPU usage response text.

    Reads the CPU usage details file being populated at the sampling
    frequency and returns the details for the current process IDs.

    cpu_usage/temp/store is the file in which the details are stored.

    @return: JSON CPU usage details object sorted by the process name.
    """
    with open(settings.STORE_FILE) as fp:
        data = fp.read()
    data = json.loads(data)
    process_details = RU.get_curr_processes(data)
    return json.dumps(sorted(process_details, key=lambda k: k['name']))


def run(server_class=HTTPServer, handler_class=CPUUsageHandler):
    """Run the web server for the application. Parallel processing of
    recording CPU usage to a file is invoked here.

    @param server_class: Server to be used. Defaults to HTTPServer. To be
        replaced for custom server class, e.g when to use threads.
    @param handler_class: Handler to be used. Defaults to the extended
        CPUUsageHandler.
    @handles KeyboardInterrupt: Terminates parallel processing and closes
        socket operation.
    """
    server_address = (settings.HOST, settings.PORT)
    httpd = server_class(server_address, handler_class)
    print settings.START_MSG
    try:
        # Parallel processing to record CPU usages to a file.
        record = Popen([sys.executable, settings.RECORD_USAGE])
        httpd.serve_forever()
    except KeyboardInterrupt:
        # Parallel processing terminated here.
        record.terminate()
        print settings.STOP_MSG
        httpd.socket.close()
    except Exception:
        raise


if __name__ == '__main__':
    run()
