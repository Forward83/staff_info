from db.connectors import connection_factory
from decouple import config

DB_CREDENTIALS = {}
DB_CREDENTIALS['host'] = config('DB_HOST')
DB_CREDENTIALS['user'] = config('DB_USER')
DB_CREDENTIALS['passwd'] = config('DB_PASSWORD')
DB_CREDENTIALS['db'] = config('DATABASE')
DB_TYPE = config('DB_TYPE')
connector = connection_factory(DB_TYPE, **DB_CREDENTIALS)
