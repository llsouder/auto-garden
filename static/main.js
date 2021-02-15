function round(value, precision) {
    var multiplier = Math.pow(10, precision || 0);
    return Math.round(value * multiplier) / multiplier;
} //borrowed from stackoverflow

function toggleLed() {
    const ledHttp = new XMLHttpRequest();
    const ledurl="http://" + location.host + "/toggle_led";
    ledHttp.open("GET", ledurl);
    ledHttp.send();
}

function update_light_indicator(light_on) {
    if(document.getElementById("myDIV")!=null) {
        if(light_on) {
          className = "greendash";
        } else {
          className = "reddash"
        }
        document.getElementById("myDIV").className = className;
        document.getElementById("myDIV").innerHTML = "Light detected?<br>" + light_on + "<br>";
    }
 }

 function update_temperature(data) {
    if(document.getElementById("tempF")!=null) {
        document.getElementById("tempF").innerHTML = round(data, 2).toFixed(2);
    }
 }

 function update_humidity(data) {
    if(document.getElementById("humidity")!=null) {
        document.getElementById("humidity").innerHTML = round(data, 2).toFixed(2);
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