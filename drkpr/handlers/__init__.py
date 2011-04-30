"""View handlers package.
"""

def includeme(config):
    """Add the application's view handlers.
    """
    config.add_handler("home", "/", "drkpr.handlers.main:Main",
                       action="index")
    config.add_handler("main", "/{action}", "drkpr.handlers.main:Main",
        path_info=r"/(?!favicon\.ico|robots\.txt|w3c)")
