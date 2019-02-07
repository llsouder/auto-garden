extern crate sysfs_gpio;

use sysfs_gpio::{Direction, Pin};
use std::thread::sleep;
use std::time::Duration;
use std::io::{self, Write};

fn main() {
    println!("Blinky, Blinky!");
    let my_led = Pin::new(8); // number depends on chip, etc.
    my_led.with_exported(|| {
        my_led.set_direction(Direction::Low)?;
        loop {
            my_led.set_value(0).expect("nope, no zero for you!");
            print!("\rOn ");
            io::stdout().flush().unwrap();
            sleep(Duration::from_millis(1000));
            my_led.set_value(1).expect("and no again!");
            print!("\rOff");
            io::stdout().flush().unwrap();
            sleep(Duration::from_millis(1000));
        }
    }).expect("can't export my led.");
}
