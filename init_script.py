import copy
import getpass
import subprocess
from db.connectors import connection_factory
from settings import DB_CREDENTIALS, DB_TYPE


admin_credential = copy.deepcopy(DB_CREDENTIALS)
del admin_credential['db']
cnx, connector = None, None

# Create connection to mysql with admin credentials
while not cnx:
    username = input('Input DB administrator username: ')
    password = getpass.getpass()
    admin_credential['user'] = username
    admin_credential['passwd'] = password
    connector = connection_factory(DB_TYPE, **admin_credential)
    cnx = connector.connection

# SQL block for DB, user, grant privileges creation
sql_create_db = "CREATE DATABASE IF NOT EXISTS {}; ".format(DB_CREDENTIALS['db'])
sql_create_user = "CREATE USER IF NOT EXISTS {}@{} IDENTIFIED BY '{}'; ".format(DB_CREDENTIALS['user'],
                                                                                DB_CREDENTIALS['host'],
                                                                                DB_CREDENTIALS['passwd'])
sql_grant_perm = "GRANT ALL PRIVILEGES ON {}.* TO {}@{};".format(DB_CREDENTIALS['db'], DB_CREDENTIALS['user'],
                                                                 DB_CREDENTIALS['host'])
for sql in (sql_create_db, sql_create_user, sql_grant_perm):
    connector.execute_sql(sql, change=False)
connector.close()

# Loading DB skeleton
args = [DB_TYPE, '-u{}'.format( admin_credential['user']), '-p{}'.format(admin_credential['passwd']),
        DB_CREDENTIALS['db'], ]
with open('db/attendance.sql') as input_file:
    proc = subprocess.Popen(args, stdin=input_file, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.communicate()
if proc.returncode == 0:
    print('DB {} was created successfully'.format(DB_CREDENTIALS['db']))






