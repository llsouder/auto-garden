#![feature(proc_macro_hygiene, decl_macro)]
#[macro_use]
extern crate rocket;
extern crate rocket_contrib;

extern crate sysfs_gpio;
extern crate ws;

use sysfs_gpio::{Direction, Pin};
use std::thread::sleep;
use std::thread::spawn;
use std::time::Duration;
use std::io::{self, Write, Result};
use rocket::State;
use rocket::response::content::Html;
use rocket::response::NamedFile;
use rocket_contrib::serve::StaticFiles;
use ws::{WebSocket, Sender};

struct Gpio {
    led: Pin,
    sensor: Pin,
}

#[get("/get_status")]
fn get_status(gpio: State<Gpio>) -> &str {
    light_status(gpio.sensor)
}

fn light_status(sensor: Pin) -> &'static str {
    let sense = sensor.get_value().unwrap();
    if sense == 0
    {
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
    }).unwrap();


    let my_led = Pin::new(20); // number depends on chip, etc.
    let my_sensor = Pin::new(21);
    my_led.export().expect("Cannot access GPIO! LED export failed");
    my_sensor.export().expect("Cannot access GPIO! sensor export failed");
    my_led.set_direction(Direction::Low).expect("fail set dir");
    my_sensor.set_direction(Direction::In).expect("fail set dir");

    // Get a sender for ALL connections to the websocket
    let broacaster = me.broadcaster();

    // Setup thread for listening to stdin and sending messages to connections
    let input = spawn(move || {
        loop {
            broacaster.send(light_status(my_sensor)).unwrap();
            sleep(Duration::from_millis(3000));
        }
    });

    spawn(move || {
        me.listen("0.0.0.0:3012").unwrap();
    });

    rocket::ignite()
        .mount("/", StaticFiles::from("static"))
        .mount("/", routes![get_status])
        .manage(Gpio { led: my_led, sensor: my_sensor })
        .launch();
    // Run the websocket
    //   input.join().unwrap();
}

fn light_detection_loop(my_led: Pin, my_sensor: Pin) {
    loop {
        let sense = my_sensor.get_value().unwrap();
        if sense == 0
        {
            my_led.set_value(1).expect("nope, no zero for you!");
            print!("\rLights Off ");
            io::stdout().flush().unwrap();
        } else {
            my_led.set_value(0).expect("nope, no zero for you!");
            print!("\rLights On ");
            io::stdout().flush().unwrap();
        }

        sleep(Duration::from_millis(250));
        my_led.set_value(0).expect("and no again!");
        io::stdout().flush().unwrap();
        sleep(Duration::from_millis(250));
    }
}
