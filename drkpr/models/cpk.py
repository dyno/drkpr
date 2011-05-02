import shlex, subprocess, os.path, sys, logging

import pyramid.threadlocal

from drkpr.lib.util import FUNC_NAME, pack_result, RS_SUCCESS, RS_FAILURE

log = logging.getLogger(__name__)

#----------------------------------------------------------------------
def run(cmd):
    try:
        args = shlex.split(cmd)
        p = subprocess.Popen(args)
        returncode = p.wait()
        if returncode == 0:
            r = pack_result(RS_SUCCESS)
    except Exception, e:
        r = pack_result(RS_FAILURE, msg=repr(e))

    log.info("%s(): %s => %s" % (FUNC_NAME(1), cmd, repr(r)))
    return r

#----------------------------------------------------------------------
#http://code.google.com/p/cpkcrypto/
def gen_master_key():
    if os.path.exists(os.path.expanduser("~/.cpk/public_params")):
        r = pack_result(RS_FAILURE, "public_params.der already imported!")
        log.info("%s(): => %s" % (FUNC_NAME(), repr(r)))
        return r

    request = pyramid.threadlocal.get_current_request()
    cmd = "%(cpk.dir)s/cpk -import-param -in %(cpk.dir)s/public_params.der" % request.registry.settings
    return run(cmd)

