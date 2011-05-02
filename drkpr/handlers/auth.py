import logging
from hashlib import md5

from pyramid_handlers import action
from pyramid.httpexceptions import HTTPFound
from sqlahelper import get_session

from drkpr.lib.util import FUNC_NAME, pack_result, RS_SUCCESS, RS_FAILURE
import drkpr.models as model
import drkpr.handlers.base as base

log = logging.getLogger(__name__)

class Auth(base.Handler):
    @action(name="display", renderer="login.mako")
    def display(self):
        if self.request.session.get("user"):
            return HTTPFound('/')
        return {}

    @action(name="login", renderer="json")
    def login(self):
        username = self.request.POST["username"]
        passwd = md5(self.request.POST["passwd"]).hexdigest()
        db_session = get_session()
        q = db_session.query(model.DKUser)
        user = q.get(username)
        if user.passwd == passwd:
            #cache user in session
            self.request.session["user"] = user
            self.request.session.save()
            return pack_result(RS_SUCCESS)
        else:
            return pack_result(RS_FAILURE)

    @action(name="logout", renderer="login.mako")
    def logout(self):
        self.request.session.clear()
        self.request.session.save()
        return {}

    @action(name="register", renderer="json")
    def register(self):
        user = model.DKUser()

        user.username = request.POST["username"]
        user.passwd = md5(request.POST["passwd"]).hexdigest()
        user.master_email = request.POST["email"]
        user.phone_mobile = request.POST["phone_mobile"]
        user.phone_office = request.POST["phone_office"]
        user.phone_home = request.POST["phone_home"]
        user.org = request.POST["org"]
        user.title = request.POST["title"]
        user.addr = request.POST["addr"]
        #roles is stored as ":" seperated string
        user.roles = ":".join((meta.ROLE_USER, ))

        db_session = get_session()
        db_session.add(user)
        return pack_result(RS_SUCCESS)


