"""Create the application's database.

Run this once after installing the application::

    python -m drkpr.scripts.create_db development.ini
"""
import logging.config
import sys
import hashlib

from pyramid.paster import get_app
import sqlahelper
import sqlalchemy
import transaction

import drkpr.models as model

def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python -m drkpr.scripts.create_db INI_FILE")
    ini_file = sys.argv[1]
    logging.config.fileConfig(ini_file)
    log = logging.getLogger(__name__)
    app = get_app(ini_file, "myapp")
    settings = app.registry.settings

    engine = sqlalchemy.engine_from_config(settings, prefix="sqlalchemy.",
                pool_recycle=3600, convert_unicode=True)
    sqlahelper.add_engine(engine)
    Base = sqlahelper.get_base()
    Session = sqlahelper.get_session()

    # Create the tables if they don't already exist
    log.info("Initialize database ...")
    Base.metadata.create_all(bind=Session.bind, checkfirst=True)

    #create default privileges
    log.info("Populate default privileges ...")
    log.info("nothing here...")
    log.info("Populate default privileges done.")

    #create default roles
    log.info("Populate default roles ...")
    q = Session.query(model.DKRole)
    if not q.all():
        records = [ model.DKRole(model.ROLE_SYSADMIN),
                model.DKRole(model.ROLE_USER),
        ]
        Session.add_all(records)
        log.info("Populate default roles done.")
    else:
        log.info("Roles already exist.")

    log.info("Populate default roles done.")

    #create default system parameters
    log.info("Populate default system parameters ...")
    q = Session.query(model.DKSystem)
    if not q.all():
        records = [ model.DKSystem("master_key_status", model.SS_SERVICE_NO_KEY),
                model.DKSystem("service_key_gen_status", model.SS_SERVICE_NOT_AVAIL),
                model.DKSystem("service_key_revoke_status", model.SS_SERVICE_NOT_AVAIL),
        ]
        Session.add_all(records)
        log.info("Populate default system parameters done.")
    else:
        log.info("System parameters exists.")

    #create default admin account
    log.info("Create default admin account ...")
    q = Session.query(model.DKUser)
    r = q.get("sysadmin")
    if not r:
        user = model.DKUser()
        user.username = "sysadmin"
        user.roles = ":".join(["", model.ROLE_SYSADMIN, ""])
        user.passwd = hashlib.md5("sysadmin").hexdigest()
        user.master_email = "sysadmin@example.com"
        user.actived = True
        Session.add(user)
        log.info("Admin account setup complete.")
    else:
        log.info("Admin account already setup.")

    transaction.commit()

if __name__ == "__main__":
    main()

