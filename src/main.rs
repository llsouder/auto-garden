extern crate sysfs_gpio;

use sysfs_gpio::{Direction, Pin};
use std::thread::sleep;
use std::time::Duration;
use std::io::{self, Write};

fn main() {
    println!("Blinky, Blinky!");
    let my_led = Pin::new(20); // number depends on chip, etc.
    let my_sensor = Pin::new(21);
    my_led.export().unwrap();
    my_sensor.export().unwrap();
	my_led.set_direction(Direction::Low).unwrap();
	my_sensor.set_direction(Direction::In).unwrap();
	loop {
		let sense = my_sensor.get_value().unwrap();
		if sense == 0
		{
			my_led.set_value(1).expect("nope, no zero for you!");
			print!("\rLights Off ");
			io::stdout().flush().unwrap();
		}
		else 
		{
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
