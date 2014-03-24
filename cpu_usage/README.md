#CPU USAGE

A pythonic web application that displays CPU usage of processes on a machine.

The application samples the CPU usage of all processes running on the server (similar to the 'top' command on the UNIX like systems) at the frequency of 1 second. It also maintains running averages of the CPU usage for each process over the past 60 seconds. The information collected about the CPU usage is then displayed as a GET XHR.

The webapp doesn't use any web frameworks like Django. Neither does the implementation use external libraries for client side implementation. Back-end is pure python. Front-end is Javascript and HTML5.


##BUILD & Run(Install) Instructions

+ You would need to have ```setuptools``` installed in your system for this. If you don't have one, follow the <a href="https://pypi.python.org/pypi/setuptools#id140" target="_blank">link</a>. Else skip the step.
+ Clone the project and change path to the ```CPU_USAGE/cpu_usage``` directory.
+ Build & Install the application using: ```sudo python setup.py install```
+ Run the command from the console: ```python -m app.server```

Application is ready and set up. Goto the browser and open the link ```http://localhost:8845/stats```


Refer [DOCS](docs/) for details of the application.
