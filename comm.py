"COMM monitor"
import time

import ingrex
import sqlite3

import logging


def main():
    """main function"""
    field = {
        'minLngE6': 115513544,
        'minLatE6': 39532744,
        'maxLngE6': 117360226,
        'maxLatE6': 40405559,
    }
    conn = sqlite3.connect('ingrex.db')
    c = conn.cursor()

    # Create table
    c.execute('''CREATE TABLE IF NOT EXISTS `message` (
        `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        `timestamp`	INTEGER NOT NULL,
        `text`	TEXT NOT NULL,
        `guid`	TEXT NOT NULL,
        `team`	TEXT NOT NULL
    );''')

    c.execute('''CREATE TABLE IF NOT EXISTS `mints` (
        `id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        `mints`	INTEGER NOT NULL
    );''')

    conn.commit()

    logging.basicConfig(filename='ingrex.log',level=logging.DEBUG)

    with open('cookies') as cookies:
        cookies = cookies.read().strip()

    mints = 1519708353697

    while True:
        intel = ingrex.Intel(cookies, field)
        result = intel.fetch_msg(mints=-1, maxts=mints)
        if result:
            mints = result[-1][1] - 1
            print(mints)
            c.execute(
                'INSERT INTO mints(`mints`)  VALUES (?)',
                (mints, ))
            conn.commit()

            for item in reversed(result[::-1]):
                message = ingrex.Message(item)
                print(u'{} {}'.format(message.time, message.text))

                c.execute(
                    'INSERT INTO message(`timestamp`, `text`, `guid`, `team`)  VALUES (?, ?, ?, ?)',
                    (message.timestamp, message.text, message.guid, message.team, ))
                conn.commit()

            time.sleep(2)


if __name__ == '__main__':
    main()
