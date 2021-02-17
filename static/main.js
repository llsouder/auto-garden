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
    const GREEN = "#73AD21";
    const RED = "#AD7321";
    if(document.getElementById("status")!=null) {
        let background = light_on ? GREEN : RED;
        document.getElementById("status").style.background = background;
        document.getElementById("status").innerHTML = "Light detected?<br>" + light_on + "<br>";
    }
 }

 function update_field(id, data) {
  if(document.getElementById(id)!=null) {
      document.getElementById(id).innerHTML = round(data, 2).toFixed(2);
  }
}

const update_temperature = update_field.bind(null, "tempF");
const  update_humidity = update_field.bind(null, "humidity")

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