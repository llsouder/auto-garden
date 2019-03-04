extern crate rusqlite;

use rusqlite::{Connection, Result, NO_PARAMS};

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
}