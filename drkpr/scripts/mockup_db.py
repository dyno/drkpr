"""Populate the application's database with mockup data.

Run this once after installing the application::

    python -m drkpr.scripts.mockup_db development.ini
"""
import sys
import random
import logging.config
import hashlib
from os.path import dirname, join

from pyramid.paster import get_app
import sqlahelper
import sqlalchemy
import transaction

import drkpr.models as model

sur_names = []
given_names = []

def load_names():
    cur_dir = dirname(__file__)
    with open(join(cur_dir, "surname_cn.txt")) as f:
        for line in f:
            if not line.startswith("#") and line.strip():
                sur_names.append(line.split()[1].lower().replace("'", ""))

    with open(join(cur_dir, "givenname_cn.txt")) as f:
        for line in f:
            if not line.startswith("#") and line.strip():
                given_names.append(line.split()[1].lower().replace("'",""))

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

    log.info("Create testing user accounts ...")
    random.seed("whatever")
    for i in range(0,100):
        sur_name = sur_names[random.randint(0, len(sur_names)-1)]
        given_name = given_names[random.randint(0, len(given_names)-1)]
        username = "%s.%s" % (sur_name, given_name)
        try:
            q = Session.query(model.DKUser)
            r = q.get(username)
            if not r:
                user = model.DKUser()
                user.username = username
                user.roles = ":".join(["", model.ROLE_USER, ""])
                user.passwd = hashlib.md5("cpksecurity").hexdigest()
                user.master_email = "%s@cpksecurity.com" % username
                user.actived = True
                Session.add(user)
                log.info(" Account '%s' setup complete." % username)
            else:
                log.info("Account '%s' already setup." % username)
        except Exception, e:
            print e

    transaction.commit()

if __name__ == "__main__":
    load_names()
    main()

