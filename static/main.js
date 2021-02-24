function round(value, precision) {
  var multiplier = Math.pow(10, precision || 0);
  return Math.round(value * multiplier) / multiplier;
} //borrowed from stackoverflow

function toggleLed() {
  const ledHttp = new XMLHttpRequest();
  const ledurl = "http://" + location.host + "/toggle_led";
  ledHttp.open("GET", ledurl);
  ledHttp.send();
}

function update_light_indicator(light_on) {
  const GREEN = "#73AD21";
  const RED = "#AD7321";
  if (document.getElementById("status") != null) {
    let background = light_on ? GREEN : RED;
    document.getElementById("status").style.background = background;
    document.getElementById("status").innerHTML = "Light detected?<br>" + light_on + "<br>";
  }
}

function update_field(id, data) {
  if (document.getElementById(id) != null) {
    document.getElementById(id).innerHTML = round(data, 2).toFixed(2);
  }
}

const update_temperature = update_field.bind(null, "temp");
const update_humidity = update_field.bind(null, "humidity")

async function update_stats() {
  function stats(arr, attribute) {
    const attributes = arr.map(obj => obj[attribute]);
    return {
      min: Math.min(...attributes),
      max: Math.max(...attributes),
      avg: attributes.reduce((a, b) => a + b, 0) / attributes.length
    };
  }

  function update_fields(stats, id)
  {
    document.getElementById("min-" + id).innerText = stats.min;
    document.getElementById("max-" + id).innerText = stats.max;
    document.getElementById("avg-" + id).innerText = stats.avg;
  }

  const sensorLog = await fetch('/sensor_log').then(resp => resp.json());
  const temp_stats = stats(sensorLog, 'temperature');
  const humidity_stats = stats(sensorLog, 'humidity');
  update_fields(temp_stats, "temp");
  update_fields(humidity_stats, "humidity");  
}

const Http = new XMLHttpRequest();
Http.onreadystatechange = (e) => {
  update_light_indicator(Http.responseText);
}

$(document).ready(function () {
  var socket = io.connect('http://' + document.domain + ':' + location.port);
  socket.on('light status', function (msg) {
    update_light_indicator(msg.data)
  });
  socket.on('current temp', function (msg) {
    update_temperature(msg.data)
  });
  socket.on('current humidity', function (msg) {
    update_humidity(msg.data)
  });
  update_stats();
});