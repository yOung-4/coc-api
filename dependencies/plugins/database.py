from pony import orm
from dependencies.get_plugins import get_env

orm.set_sql_debug(True)

get_env = get_env()

db = orm.Database()
db.bind(
    provider=get_env.provider,
    user=get_env.database_user,
    password=get_env.password,
    host=get_env.host,
    database=get_env.database,
)
