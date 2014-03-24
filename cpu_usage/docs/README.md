##Server Components

Application runs as a web server. It listens to port 8845 for **HTTP GET** requests. When it gets a request for ```/cpu_usage``` it returns the details for each process which includes:

	PID : Process ID
	NAME : Process Name
	USER TIME : Current user time average, computed over 60 seconds.
	SYSTEM TIME : Current system time average, computed over 60 seconds.
	STATUS : Current status of the process.

The information is transmitted to the client in JSON format.


##Client Components

The user interface [```stats.html```](../static/stats.html) is served by the server on a request from ```/stats```. It then fires a GET XHR to ```/cpu_usage``` which in turn creates a table and displays the JSON format _CPU USAGE_ information obtained from the server. The content of the table is refreshed every second without entire page load. The page subresources viz.  [```client.css```](../static/client.css) and [```client.js```](../static/client.js) are also served by the server. The entire implementation is in HTML5 and Javascript. No external libraries have been used in the implementation.

The application has been developed on Google Chrome as a browser.


##Implementation
Script implementation can be found [HERE](../app/).

+ A server is run using the ```BaseHTTPServer``` python library. GET method of the handler is over-ridden.
+ Simultaneously another python process ```record_usage.py``` is invoked using ```subprocess.POPEN``` until the server is closed. The script maintains details for the processes at an interval of sampling frequency.
+ The script above also records cpu times for the processes in a queue per process. The length of the queue is interval over which the average is to be calculated.
+ After the processing is done the results are written into a JSON file.

When looked from Client's perspective, it fires series of XHRs at an interval of 1 second.

+ When the app gets one of those XHRs from the client, it opens the JSON file and uses the details stored there to retrieve details for all processes it finds running then.
+ The fetched details are JSONified and the response text is sent to the Client.
+ Client iterates over the object and prepares the table of results.


##Assumptions

No assumptions as such. However, following points needs to be mentioned here.

+ A process is distinguished by its PID and not its name.
+ Only the processes at the time an XHR is fired are displayed.
+ States are ignored. Sleeping, Disk-sleeping, Running etc. all are displayed.


**Tests** can be found [HERE](../tests/)

