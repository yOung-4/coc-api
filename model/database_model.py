from pony import orm
from dependencies.plugins.database import db


class Database_sign_up_request(db.Entity):
    id = orm.PrimaryKey(int, auto=True)
    email = orm.Required(str)
    password = orm.Required(str)
    nick_name = orm.Required(str)


db.generate_mapping(create_tables=True)
