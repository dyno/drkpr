import logging
import sys, os.path

from pyramid_handlers import action
from pyramid.httpexceptions import HTTPFound

import drkpr.handlers.base as base
import drkpr.models as model
import drkpr.models.cpk as cpk

log = logging.getLogger(__name__)

class Main(base.Handler):
    @action(renderer="main.mako")
    def index(self):
        log.debug("main.Main.index():")

        if not self.request.session.get("user"):
            return HTTPFound(location=self.request.route_path("auth", action="display"))

        # Return a dict of template variables for the renderer.
        return {"project":"drkpr"}

    @action(name="gen_master_key", renderer="json")
    def gen_master_key(self):
        if not self.request.session.get("user"):
            raise Exception("not logged in!")

        return cpk.gen_master_key()

