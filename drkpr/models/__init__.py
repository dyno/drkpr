import logging
from sqlalchemy import orm, schema, types
from sqlalchemy.schema import Table, Column, ForeignKey
import sqlahelper
import transaction

log = logging.getLogger(__name__)

Base = sqlahelper.get_base()
metadata = Base.metadata

# constants
# dk_system SS=>System Status
# config status
SS_SERVICE_NO_KEY       = "NOKEY"
SS_SERVICE_AVAIL        = "AVAILABLE"
SS_SERVICE_NOT_AVAIL    = "N/A"
#FIXME: not sure if running status is needed.

# system roles
ROLE_SYSADMIN   = "SYSADMIN"
ROLE_USER       = "USER"

# tables
user_table = Table("dk_user", metadata,
        Column("username", types.String(32), primary_key=True),
        Column("passwd", types.String(64)),
        #
        Column("roles", types.String(256)),
        #can be calculated from role, cache it.
        Column("privileges", types.String(256)),
        #
        Column("master_email", types.String(128), nullable=False, index=True),
        Column("second_email", types.String(128)),
        Column("hasmore_email", types.Boolean, default=False),
        #
        Column("phone_mobile", types.String(32)),
        Column("phone_home", types.String(32)),
        Column("phone_office", types.String(32)),
        Column("hasmore_phone", types.Boolean, default=False),
        #
        Column("master_key", types.Text),
        #
        Column("name", types.String(128)),
        Column("title", types.String(128)),
        Column("org", types.String(128)),
        Column("addr", types.String(256)),
        #
        Column("actived", types.Boolean, default=False),
)

userinfo_table = Table("dk_userinfo", metadata,
        Column("id", types.Integer, primary_key=True),
        Column("username", types.String(32), ForeignKey("dk_user.username")),
        #0.5 does not have Enum, http://www.sqlalchemy.org/trac/wiki/06Migration#GenericEnumType
        #Column("infotype", types.Enum(["EMAIL","PHONE", "OTHER"])),
        Column("infotype", types.String(8)),
        Column("info", types.TEXT)
)

privilege_table = Table("dk_privilege", metadata,
        Column("name", types.String(32), primary_key=True, nullable=False),
        Column("display_name", types.String(32)),
        Column("desc", types.TEXT),
)

role_table = Table("dk_role", metadata,
        Column("name", types.String(32), primary_key=True, nullable=False),
        Column("display_name", types.String(32)),
        Column("desc", types.TEXT),
)

role_priv_table = Table("dk_role_priv", metadata,
        Column("role", types.String(32), ForeignKey("dk_role.name")),
        Column("priv", types.String(32), ForeignKey("dk_privilege.name"))
)

history_table = Table("dk_history", metadata,
        Column("id", types.Integer, primary_key=True),
        #when the log entry created, dttm -> datetime
        Column("dttm", types.DateTime, nullable=False),
        Column("username", ForeignKey("dk_user.username")),
        Column("operation", types.String(32), nullable=False),
        Column("detail", types.Text),
        #use sqlite autoincrement feature, http://www.sqlite.org/autoinc.html
        # http://www.sqlalchemy.org/docs/dialects/sqlite.html#auto-incrementing-behavior
        sqlite_autoincrement=True,
)

system_table = Table("dk_system", metadata,
        Column("key", types.String(32), primary_key=True),
        Column("val", types.String(32)),
)

class DKUser(object):
    pass

class DKUserInfo(object):
    pass

class DKRole(object):
    def __init__(self, name):
        self.name = name

class DKPrivilege(object):
    def __init__(self, name):
        self.name = name

class DKHistory(object):
    pass

class DKSystem(object):
    def __init__(self, key, val):
        self.key = key
        self.val = val

# http://www.sqlalchemy.org/docs/orm/mapper_config.html
orm.mapper(DKUser, user_table, properties={
        "history": orm.relation(DKHistory, backref="user", lazy="select")})
orm.mapper(DKUserInfo, userinfo_table)
orm.mapper(DKRole, role_table,
        properties={"privildeges": orm.relation(DKPrivilege, secondary=role_priv_table)})
orm.mapper(DKPrivilege, privilege_table)
orm.mapper(DKHistory, history_table)
orm.mapper(DKSystem, system_table)

