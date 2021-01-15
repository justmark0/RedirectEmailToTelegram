from datetime import datetime
from pony.orm import *

db = Database()


class User(db.Entity):
    user_id = Required(int, size=64)
    last_seen = Required(datetime, auto=True)
    email = Required(str)
    password = Required(str)
