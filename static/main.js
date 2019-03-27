function toggleLed() {
    const ledHttp = new XMLHttpRequest();
    const ledurl="http://" + location.host + "/toggle_led";
    ledHttp.open("GET", ledurl);
    ledHttp.send();
}

function update_light_indicator(signal_text) {
    console.log("update_light_indicator:" + signal_text);
    if(document.getElementById("myDIV")!=null) {
        document.getElementById("myDIV").innerHTML = signal_text + "<br>";
        if(signal_text.includes("On")) {
          document.getElementById("myDIV").className = "greendash";
        } else {
          document.getElementById("myDIV").className = "reddash";
        }
    }
 }

 const Http = new XMLHttpRequest();
 Http.onreadystatechange=(e)=>{
   console.log("onreadystatechange" + e);
   update_light_indicator(Http.responseText);
 }

 //return a one time light status
 const url="http://" + location.host + "/get_status";
 Http.open("GET", url);
 Http.send();

$(document).ready(function() {
  var socket = io.connect('http://' + document.domain + ':' + location.port);
  socket.on('light status', function(msg){
    console.log('light status:' + msg.data);
    update_light_indicator(msg.data)
  });
  socket.on('number', function(msg){
    console.log('I got a number:' + msg.data);
  });
});