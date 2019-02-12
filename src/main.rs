#![feature(proc_macro_hygiene, decl_macro)]
#[macro_use]
extern crate rocket;
extern crate rocket_contrib;

extern crate sysfs_gpio;
extern crate ws;

use rocket::State;
use rocket_contrib::serve::StaticFiles;
use std::thread::sleep;
use std::thread::spawn;
use std::time::Duration;
use sysfs_gpio::{Direction, Pin};

struct Gpio {
    sensor: Pin,
}

#[get("/get_status")]
fn get_status(gpio: State<Gpio>) -> &str {
    light_status(gpio.sensor)
}

fn light_status(sensor: Pin) -> &'static str {
    let sense = sensor.get_value().unwrap();
    if sense == 0 {
        "Lights Off "
    } else {
        "Lights On "
    }
}

fn main() {
    // Create simple websocket that just prints out messages
    let me = ws::WebSocket::new(|_| {
        move |msg| {
            println!("Peer {} got message: {}", "Happy", msg);
            Ok(())
        }
    })
    .unwrap();
   let my_sensor = Pin::new(21);
    my_sensor
        .export()
        .expect("Cannot access GPIO! sensor export failed");
    my_sensor
        .set_direction(Direction::In)
        .expect("fail set dir");

    // Get a sender for ALL connections to the websocket
    let broadcaster = me.broadcaster();

    // Setup thread for listening to stdin and sending messages to connections
    let input = spawn(move || loop {
        broadcaster.send(light_status(my_sensor)).unwrap();
        sleep(Duration::from_millis(3000));
    });

    spawn(move || {
        me.listen("0.0.0.0:3012").unwrap();
    });

    rocket::ignite()
        .mount("/", StaticFiles::from("static"))
        .mount("/", routes![get_status])
        .manage(Gpio {
            sensor: my_sensor,
        })
        .launch();
    // Run the websocket
    input.join().unwrap();
}
