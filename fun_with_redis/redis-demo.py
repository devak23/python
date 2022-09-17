import datetime
from datetime import timedelta
import random

import redis

r = redis.Redis()

r.mset({'Croatia': 'Zagreb', 'Bahamas': 'Nassau', 'India': 'New Delhi', 'Norway': 'Oslo', 'Finland': 'Helsinki'})

print(r.ping())
print(r.get('India'))
print(r.get('Bahamas').decode('utf8'))

# -------------------------------------------------------
today = datetime.date.today()
stoday = today.isoformat()
print(stoday)

visitors = {'Guru', 'Tejas', 'Srini'}
r.sadd(stoday, *visitors)
print(r.smembers(stoday))
print(r.scard(today.isoformat()))

# -------------------------------------------------------
random.seed(737)
inventory = {f"inventory:{random.getrandbits(32)}": i for i in (
    {
        "color": "black",
        "price": 49.99,
        "style": "fitted",
        "quantity": 1000,
        "npurchased": 0,
    },
    {
        "color": "maroon",
        "price": 59.99,
        "style": "hipster",
        "quantity": 500,
        "npurchased": 0,
    },
    {
        "color": "green",
        "price": 99.99,
        "style": "baseball",
        "quantity": 200,
        "npurchased": 0,
    }
)}

r = redis.Redis(db=1)

with r.pipeline() as pipe:
    for invetory_id, item in inventory.items():
        pipe.hmset(invetory_id, item)
    pipe.execute()

r.bgsave()

# -------------------------------------------------------
print("keys: ", r.keys())
print("hgetall: ", r.hgetall("inventory_id:11934279"))
print("quantity decremented: ",r.hincrby("inventory_id:11934279", "quantity", -1))
print("purchased incremented: ", r.hincrby("inventory_id:11934279", "npurchased", 1))

# -------------------------------------------------------
# setting up key expiry
r.setex("runner", timedelta(minutes=1), value="abracadabra")
print ("time to live: runner = ", r.ttl("runner"))

r.expire("runner", timedelta(seconds=3))

