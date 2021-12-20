import schedule
import time

import ALLTHAIEVENT
import EVENTPOP
import IMPACT
import ZIPEVENT

# -- Start Schedule

# 01 AM (18.00)
schedule.every().day.at("18:00").do(ALLTHAIEVENT)

# 02 AM (19.00)
schedule.every().day.at("19:00").do(EVENTPOP)

# 03 AM (20.00)
schedule.every().day.at("20:00").do(IMPACT)

# 04 AM (21.00)
schedule.every().day.at("21:00").do(ZIPEVENT)

while True:
    schedule.run_pending()
    time.sleep(1)
