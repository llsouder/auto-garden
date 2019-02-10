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

    var ws = new WebSocket("ws://" + location.hostname + ":3012");
    ws.onmessage = function (evt) {
     update_light_indicator(evt.data);
    }
    const Http = new XMLHttpRequest();
    Http.onreadystatechange=(e)=>{
      update_light_indicator(Http.responseText);
    }
    const url="http://" + location.host + "/get_status";
    Http.open("GET", url);
    Http.send();