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
use std::sync::atomic::{AtomicBool, Ordering};
use std::time::Duration;
use sysfs_gpio::{Direction, Pin};

mod db;

use rusqlite::Connection;

struct Resources {
    led: Pin,
    sensor: Pin,
    led_status: AtomicBool,
}

fn get_connection() -> Connection {
    Connection::open("auto-garden.db")
        .expect("Could not open auto-garden.db")
}

#[get("/toggle_led")]
fn toggle_led(gpio: State<Resources>) {
    if gpio.led_status.load(Ordering::Relaxed) {
        println!("Turn LED Off");
        gpio.led.set_value(0).unwrap();
        gpio.led_status.store(false, Ordering::Relaxed);
    } else {
        println!("Turn LED On");
        gpio.led.set_value(1).unwrap();
        gpio.led_status.store(true, Ordering::Relaxed);
    }
}

#[get("/get_status")]
fn get_status(gpio: State<Resources>) -> &str {
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
    db::setup_db(&get_connection()).expect("Cannot setup database.");

    let my_led = Pin::new(20);
    my_led
        .export()
        .expect("Cannot access GPIO! LED export failed");
    my_led
        .set_direction(Direction::Low)
        .expect("fail set dir");

    let my_sensor = Pin::new(21);
    my_sensor
        .export()
        .expect("Cannot access GPIO! sensor export failed");
    my_sensor
        .set_direction(Direction::In)
        .expect("fail set dir");

    let web_socket = ws::WebSocket::new(|_| {
        move |msg| {
            println!("Peer {} got message: {}", "Happy", msg);
            Ok(())
        }
    }).unwrap();
    // Get a sender for ALL connections to the websocket

    // Setup thread for listening to stdin and sending messages to connections
    spawn(move || {
        web_socket.listen("0.0.0.0:3012").unwrap();
    });

    let broadcaster = web_socket.broadcaster();
    let mut previous_status = "";
    let input = spawn(move || loop {
        let status = light_status(my_sensor);
        if status != previous_status {
            broadcaster.send(status).unwrap();
            db::record_light(&get_connection(), status.contains("On"))
                .expect("Could not record light on.");
            previous_status = status;
        }
        sleep(Duration::from_millis(250));
    });
    rocket::ignite()
        .mount("/", StaticFiles::from("static"))
        .mount("/", routes![get_status])
        .mount("/", routes![toggle_led])
        .manage(Resources {
            led: my_led,
            led_status: AtomicBool::new(false),
            sensor: my_sensor,
        })
        .launch();
    // Run the websocket
    input.join().unwrap();
}
