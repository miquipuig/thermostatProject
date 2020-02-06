import numpy as np
from datetime import datetime,timedelta

tm=datetime.now()

#classic round 5 minutes
tm += timedelta(minutes=5)
print(tm)
tm -= timedelta(minutes=tm.minute % 10,seconds=tm.second, microseconds=tm.microsecond)
print(tm)

tm=datetime.now()                         
print(tm)
tm += timedelta(minutes=0.5) 
tm -= timedelta(minutes=tm.minute % 1, seconds=tm.second, microseconds=tm.microsecond)
print(tm)

# Función general para redondear una fecha y hora en cualquier lapso de tiempo en segundos:

tm=datetime.now()
print(tm)
discard = timedelta(minutes=tm.minute % 1, seconds=tm.second,microseconds=tm.microsecond)
tm -= discard
if discard >= timedelta(minutes=0.5):
    tm += timedelta(minutes=1)
print(tm)