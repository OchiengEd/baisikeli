#!/usr/bin/env python3
from datetime import datetime
import schedule
import time

def synchronize():
    print(datetime.now())

def main():
    keep_running = True
    schedule.every(interval=1).hours.do(synchronize)

    while keep_running:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt as ki:
            keep_running = False
            print(ki)
        except Exception as e:
            keep_running = False
            print(e.getMessage())

if __name__ == '__main__':
    main()
