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
    document.getElementById(id).innerHTML = round(data, 1).toFixed(1);
  }
}

const update_temperature = update_field.bind(null, "temp");
const update_humidity = update_field.bind(null, "humidity")

function update_stats(sensor_log) {
  function stats(arr, attribute) {
    const attributes = arr.map(obj => obj[attribute]);
    return {
      min: round(Math.min(...attributes), 1),
      max: round(Math.max(...attributes), 1),
      avg: round(attributes.reduce((a, b) => a + b, 0) / attributes.length, 1)
    };
  }

  function update_stat_fields(stats, id) {
    document.getElementById("min-" + id).innerText = stats.min;
    document.getElementById("max-" + id).innerText = stats.max;
    document.getElementById("avg-" + id).innerText = stats.avg;
  }

  const temp_stats = stats(sensor_log, 'temperature');
  const humidity_stats = stats(sensor_log, 'humidity');
  update_stat_fields(temp_stats, "temp");
  update_stat_fields(humidity_stats, "humidity");
}

async function fetch_sensor_log_and_update() {
  function isValid(date) {
    return date.toString() !== "Invalid Date";
  }

  function format(date) {
    const hour = date.getHours();
    const min = date.getMinutes();
    const second = date.getSeconds();
    const month = date.getMonth() + 1;
    const day = date.getDate();
    const year = date.getFullYear();
    return `${year}-${month}-${day}T${hour}-${min}-${second}`
  }

  let start_date = new Date(document.getElementById("time-start").value);
  let end_date = new Date(document.getElementById("time-end").value);
  let params = {
    ...(isValid(start_date) && { start: format(start_date) }),
    ...(isValid(end_date) && { end: format(end_date) })
  };

  let url = new URL("/sensor_log", document.baseURI);
  url.search = new URLSearchParams(params).toString();
  const sensor_log = await fetch(url).then(resp => resp.json());
  update_stats(sensor_log);
}

const Http = new XMLHttpRequest();
Http.onreadystatechange = (e) => {
  update_light_indicator(Http.responseText);
}

$(document).ready(function () {
  document.getElementById("time-start").onblur = fetch_sensor_log_and_update;
  document.getElementById("time-end").onblur = fetch_sensor_log_and_update;

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
  fetch_sensor_log_and_update();
});