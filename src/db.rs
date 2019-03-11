extern crate rusqlite;
extern crate time;

use rusqlite::{Connection, Result, NO_PARAMS};
use time::Timespec;

#[derive(Debug)]
struct Light {
    id: i32,
    time_created: Timespec,
    light_on: bool,
}
pub fn setup_db(conn: &Connection) -> Result<()> {
    conn.execute(
        "create table if not exists light_sensor (
             id integer primary key,
             light_time datetime,
             light_on bool
         )",
        NO_PARAMS,
    )?;
    Ok(())
}

pub fn record_light(conn: &Connection, light_on: bool) -> Result<()> {
    conn.execute(
        "INSERT INTO light_sensor (light_time, light_on) VALUES
            (datetime('now', 'localtime'), ?1 );",&[&light_on],
    )?;
    Ok(())
}

#[cfg(test)]
mod tests {
    // Note this useful idiom: importing names from outer (for mod tests) scope.
    use super::*;

fn get_fresh_connection(db_file_name: &str) -> Connection {
    let db_path = std::path::Path::new(db_file_name);
    if  db_path.exists() {
        std::fs::remove_file(db_path).unwrap();
    }
    let conn = Connection::open(db_file_name).unwrap();
    conn
}

fn count_records(conn: &Connection) -> i32 {
    let size: i32 = conn.query_row("SELECT count(*) from light_sensor;",
                              NO_PARAMS,
                              |r| r.get(0)).unwrap();
    size
}
    #[test]
    fn test_setup_db() {
        let conn = get_fresh_connection("test1.db");
        setup_db(&conn).unwrap();
    }

    #[test]
    fn test_light() {
        let conn = get_fresh_connection("test2.db");
        setup_db(&conn).unwrap();
        record_light(&conn, true).unwrap();
        record_light(&conn, false).unwrap();
        record_light(&conn, false).unwrap();
        count_records(&conn);
        assert_eq!(3, count_records(&conn));
    }

    #[test]
    fn test_addstuff() {
        let conn = Connection::open("auto-garden.db").unwrap();

        let mut stmt = conn
            .prepare("SELECT id, light_on, light_time FROM light_sensor")
            .unwrap();
        let rows = stmt
            .query_map(NO_PARAMS, |row| Light {
                id: row.get(0),
                light_on: row.get(1),
                time_created: row.get(2),
            })
            .unwrap();
        let mut previous = Light {id: 0, time_created: Timespec::new(0, 0), light_on: false};
        for light in rows {
            let current = light.unwrap();
            println!("{} {}", previous.light_on,
                     calcMins(previous.time_created.sec, current.time_created.sec ));
            previous = current;
        }
    }
    fn calcMins(previous: i64, current: i64) -> String {
        let hr = (current - previous)/3600;
        let min = ((current - previous)/60)%60;
        let sec = (current - previous)%60;
        format!("{:02}:{:02}:{:02}", hr, min, sec)
    }
}

