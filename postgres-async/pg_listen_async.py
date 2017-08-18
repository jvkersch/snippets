""" Self-contained code example to listen for postgres events.

This is the Python 3 counterpart of

  http://bjorngylling.com/2011-04-13/postgres-listen-notify-with-node-js.html

Preconditions: create a database and a trigger with

  CREATE TABLE foo (id serial primary key, name varchar);

  CREATE FUNCTION notify_trigger() RETURNS trigger AS $$
  DECLARE
  BEGIN
    PERFORM pg_notify('watchers', TG_TABLE_NAME || ',id,' || NEW.id );
    RETURN new;
  END;
  $$ LANGUAGE plpgsql;

  CREATE TRIGGER watched_table_trigger AFTER INSERT ON bar
  FOR EACH ROW EXECUTE PROCEDURE notify_trigger();

"""

import asyncio
import psycopg2

conn = psycopg2.connect(database='jvkersch')
conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

loop = asyncio.SelectorEventLoop()
asyncio.set_event_loop(loop)


def callback():
    conn.poll()
    while conn.notifies:
        notify = conn.notifies.pop(0)
        print('NOTIFY', notify.pid, notify.channel, notify.payload)


loop.add_reader(conn, callback=callback)
cur = conn.cursor()
cur.execute("LISTEN watchers")


loop.run_forever()
