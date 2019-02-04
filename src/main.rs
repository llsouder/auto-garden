extern crate sysfs_gpio;

use sysfs_gpio::{Pin};
use std::thread::sleep;
use std::time::Duration;

fn main() {
    println!("Hello, world!");
    let my_led = Pin::new(127); // number depends on chip, etc.
    my_led.with_exported(|| {
        loop {
            my_led.set_value(0).unwrap();
            sleep(Duration::from_millis(200));
            my_led.set_value(1).unwrap();
            sleep(Duration::from_millis(200));
        }
    }).unwrap();
}
