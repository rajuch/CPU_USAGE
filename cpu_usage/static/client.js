/*
 * Script component for the webapp client.
 * @created: 21 Mar, 2014
 * @author: Anshu Kumar, <anshu.choubey@imaginea.com>
 */

/*global window*/
/*global document: false */

function InvokeXHR() {
    'use strict';
    var objectData, xmlhttp;
    if (window.XMLHttpRequest) {
        // Code for other browsers
        xmlhttp = new window.XMLHttpRequest();
    } else {
        // Code for IE 5, IE 6
        xmlhttp = new window.ActiveXObject("Microsoft.XMLHTTP");
    }

    function displayTable() {
        var i, sHtml, obj;
        sHtml = "<table><tr><th>PID</th><th>NAME</th><th>USER AVG. TIME</th><th>SYSTEM AVG. TIME</th><th>STATUS</th></tr>";
        for (i = 0; i < objectData.length; i += 1) {
            obj = objectData[i];
            sHtml += "<tr><td>" + obj.pid + "</td>";
            sHtml += "<td>" + obj.name + "</td>";
            sHtml += "<td>" + obj.user_avg + "</td>";
            sHtml += "<td>" + obj.sys_avg + "</td>";
            sHtml += "<td>" + obj.status.toUpperCase() + "</td></tr>";
        }
        sHtml += "</table>";
        document.getElementById("table").innerHTML = sHtml;
    }

    xmlhttp.onreadystatechange = function () {
        var jsonResultBuffer;
        if (xmlhttp.readyState === 4 && xmlhttp.status === 200) {
            // Receives the objectified results of the JSON request.
            jsonResultBuffer = xmlhttp.responseText;
            objectData = JSON.parse(jsonResultBuffer);
            displayTable();
        }
    }
    xmlhttp.open("GET", "cpu_usage", true);
    xmlhttp.send();
}

window.onload = InvokeXHR;
var auto_refresh = setInterval(InvokeXHR, 1000);
