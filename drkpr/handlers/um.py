import logging
from hashlib import md5

from pyramid_handlers import action
from pyramid.httpexceptions import HTTPFound
from sqlahelper import get_session

from drkpr.lib.util import FUNC_NAME, pack_result, RS_SUCCESS, RS_FAILURE
import drkpr.models as model
import drkpr.handlers.base as base


log = logging.getLogger(__name__)

class UserManagement(base.Handler):
    @action(name="get_users", renderer="json")
    def get_users(self):
        if self.request.matchdict.get("pathparams"):
            offset, size = map(int, self.request.matchdict["pathparams"])
        else:
            offset = self.request.GET["offset"]
            size = self.request.GET["size"]

        db_session = get_session()
        q = db_session.query(model.DKUser).offset(offset).limit(size)
        l = [(u.username, u.master_email) for u in q.all()]

        return pack_result(RS_SUCCESS, data=l)

    @action(name="get_user_count", renderer="json")
    def get_user_count(self):
        db_session = get_session()
        count = db_session.query(model.DKUser).count()
        return pack_result(RS_SUCCESS, data=count)

