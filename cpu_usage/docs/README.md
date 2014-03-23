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
Implementation can be found [HERE](../app/)


##Tests
Tests can be found [HERE](../tests/)


##Assumptions

Content yet to be added.


##Algorithm

Content yet to be added.
