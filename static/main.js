function toggleLed() {
    const ledHttp = new XMLHttpRequest();
    const ledurl="http://" + location.host + "/toggle_led";
    ledHttp.open("GET", ledurl);
    ledHttp.send();
}

function update_light_indicator(signal_text) {
    if(document.getElementById("myDIV")!=null) {
        document.getElementById("myDIV").innerHTML = signal_text + "<br>";
        if(signal_text.includes("On")) {
          document.getElementById("myDIV").className = "greendash";
        } else {
          document.getElementById("myDIV").className = "reddash";
        }
    }
 }

 function update_temperature(data) {
    if(document.getElementById("tempF")!=null) {
        document.getElementById("tempF").innerHTML = data;
    }
 }

 function update_humidity(data) {
    if(document.getElementById("humidity")!=null) {
        document.getElementById("humidity").innerHTML = data;
    }
 }

 const Http = new XMLHttpRequest();
 Http.onreadystatechange=(e)=>{
   update_light_indicator(Http.responseText);
 }

$(document).ready(function() {
  var socket = io.connect('http://' + document.domain + ':' + location.port);
  socket.on('light status', function(msg){
    update_light_indicator(msg.data)
  });
  socket.on('current temp', function(msg){
    update_temperature(msg.data)
  });
  socket.on('current humidity', function(msg){
    update_humidity(msg.data)
  });
});