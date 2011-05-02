"""View handlers package.
"""

def includeme(config):
    """Add the application's view handlers.
    """
    # http://docs.pylonsproject.org/projects/pyramid/1.0/narr/urldispatch.html
    # http://docs.pylonsproject.org/projects/pyramid_handlers/dev/api.html
    config.add_handler("home", "/", "drkpr.handlers.main:Main",
                       action="index")

    config.add_handler("main", "/{action}", "drkpr.handlers.main:Main",
        path_info=r"/(?!favicon\.ico|robots\.txt|w3c)")

    config.add_handler("auth", "/auth/{action}", "drkpr.handlers.auth.Auth")

    config.add_handler("um", r"/um/{action}*pathparams", "drkpr.handlers.um.UserManagement")

