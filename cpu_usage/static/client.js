/*
 * Script component for the webapp client.
 * @created: 21 Mar, 2014
 * @author: Anshu Kumar, <anshu.choubey@imaginea.com>
 * 
 * @todo(Run JSLINT)
 */

function InvokeXHR() {
	var objectData; // Receives the objectified results of the JSON request.
	var xmlhttp;
	if (window.XMLHttpRequest) {
		// Code for other browsers
		xmlhttp = new XMLHttpRequest();
	} else {
		// Code for IE 5, IE 6
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}
	xmlhttp.onreadystatechange = function() {
		if (xmlhttp.readyState==4 && xmlhttp.status==200) {
            var jsonResultBuffer = xmlhttp.responseText;
            objectData = JSON.parse(jsonResultBuffer);
            DisplayTable();
		}
	}
	xmlhttp.open("GET", "cpu_usage", true);
	xmlhttp.send();

    function DisplayTable() {
        var sHtml = "<table><tr><th>PID</th><th>NAME</th><th>USER AVG. TIME</th><th>SYSTEM AVG. TIME</th><th>STATUS</th></tr>";
        for (i=0; i<objectData.length; i++) {
        	obj = objectData[i]
            sHtml += "<tr><td>" + obj.pid + "</td>";
            sHtml += "<td>" + obj.name + "</td>";
            sHtml += "<td>" + obj.user_avg + "</td>";
            sHtml += "<td>" + obj.sys_avg + "</td>";
            sHtml += "<td>" + obj.status.toUpperCase() + "</td></tr>";
        }
        sHtml += "</table>";
        document.getElementById("table").innerHTML = sHtml;
    }    
}
window.onload = InvokeXHR;
var auto_refresh = setInterval(InvokeXHR, 1000);