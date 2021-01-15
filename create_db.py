from data.models import db
from data.config import DB_SETTINGS


settings = DB_SETTINGS.split(":")
if settings[0] == 'sqlite':
    db.bind('sqlite', DB_SETTINGS.split(":")[1], create_db=True)
    db.generate_mapping(create_tables=True)
else:
    raise Exception("Configure .env file to create sqlite database")
