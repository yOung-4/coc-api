from pony import orm
from dependencies.plugins.database import db


class Database_auth_user_list(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    email = orm.Required(str)
    password = orm.Required(str)
    nick_name = orm.Required(str)


db.generate_mapping(create_tables=True)
