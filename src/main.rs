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

struct Gpio {
    led: Pin,
    sensor: Pin,
    led_status: AtomicBool,
}

#[get("/toggle_led")]
fn toggle_led(gpio: State<Gpio>) {
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
    }).unwrap();

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

    // Get a sender for ALL connections to the websocket
    let broadcaster = me.broadcaster();

    // Setup thread for listening to stdin and sending messages to connections
    let mut alternate = "Lights On";
    let input = spawn(move || loop {
        //broadcaster.send(light_status(my_sensor)).unwrap();
        broadcaster.send(alternate).unwrap();
        if alternate.contains("On") {
            alternate = "Lights Off";
        } else {
            alternate = "Lights On";
        }
        sleep(Duration::from_millis(3000));
    });

    spawn(move || {
        me.listen("0.0.0.0:3012").unwrap();
    });

    rocket::ignite()
        .mount("/", StaticFiles::from("static"))
        .mount("/", routes![get_status])
        .mount("/", routes![toggle_led])
        .manage(Gpio {
            led: my_led,
            led_status: AtomicBool::new(false),
            sensor: my_sensor,
        })
        .launch();
    // Run the websocket
    input.join().unwrap();
}
