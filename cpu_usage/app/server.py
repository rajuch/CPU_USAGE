'''Application web server.

@created: Mar 21, 2014
@author: Anshu Kumar, <anshu.choubey@imaginea.com>

@todo(Implement Logging)
'''

# pylint: disable=C0103

import json
import os

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from threading import Lock, Thread
from mimetypes import types_map

from record_usage import RecordUsage as RU
import settings


class CPUUsageHandler(BaseHTTPRequestHandler):
    """Extended handler class for the web server."""

    def do_GET(self):
        """Over-ridden GET method."""
        self.path = self.path.rstrip('/')
        print "Path: ", self.path
        if self.path.endswith('favicon.ico'):
            self.send_error(settings.HTTP_NOT_FOUND)
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
        if ext in ('.html', '.css', '.js'):
            self.fetch_file(
                os.path.join(settings.STATIC_PATH, self.path.lstrip('/')),
                types_map[ext])
        else:
            # Unknown requests.
            self.send_error(settings.HTTP_NOT_FOUND)

    def fetch_file(self, path, content_type, response=settings.HTTP_OK):
        """Fetch response from a file to the client.

        Invokes fetch_content method after IO operation on the file.
        @param path: File path.
        @param content_type: Content type for the file.
        @param response: Response code. Defaults to 200(Successful).
        @handles IOError: Send 500 error to the client.
        """
        try:
            with open(path) as fp:
                self.fetch_content(fp.read(), content_type, response)
        except IOError:
            self.send_error(settings.HTTP_INTERNAL_SERVER_ERROR)

    def fetch_content(self, content, content_type='text/html',
                      response=settings.HTTP_OK):
        """Fetch response to the client.

        @param content: Content to be fetched.
        @param content_type: Type of the content. Defaults to text/html.
        @param response: Response code. Defaults to 200(Successful).
        """
        self.send_response(response)
        self.send_header('Content-type', content_type)
        self.end_headers()
        self.wfile.write(content)
        self.wfile.close()


def get_cpu_usage():
    """Returns the JSON format CPU usage details for current processes.
    @return: Response text. Results are sorted by the process name.
    """
    process_details = RU_OBJ.get_curr_processes()
    return json.dumps(sorted(process_details, key=lambda k: k['name']))


def run(server_class=HTTPServer, handler_class=CPUUsageHandler):
    """Run the web server for the application.

    @param server_class: Server to be used. Defaults to HTTPServer.
    @param handler_class: Handler to be used. Defaults to the extended
        CPUUsageHandler.
    @handles KeyboardInterrupt: Closes socket operation and stops the server.
    """
    server_address = (settings.HOST, settings.PORT)
    httpd = server_class(server_address, handler_class)
    print settings.START_MSG
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.socket.close()
        print settings.STOP_MSG
    except Exception:
        raise


if __name__ == '__main__':
    RU_OBJ = RU(settings.SAMPLING_FREQ, settings.AVG_INTERVAL, Lock())
    # Record CPU usage in a thread.
    ru_thread = Thread(target=RU_OBJ.record)
    ru_thread.daemon = True
    ru_thread.start()

    # Run server.
    run()
