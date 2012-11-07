"""
    Web App Launcher
"""
import cherrypy
import traceback
from chatpanel.index import Root
from chatlib import chatparam
from chatpanel import initloader
from chatpanel import *
from db import dboperations
from chatlib import chatapiserver

def run():
    initloader(chatparam.OTS_ROOT_DIR)
    root = Root()
    config = {
        'global' : {
            'server.socket_host' : '0.0.0.0',
            'server.socket_port' : chatparam.OTS_HOST_PORT,
            'server.thread_pool' : 10,
            'engine.autoreload_on' : True
            },
        '/' : {
            'tools.staticdir.root'   : chatparam.OTS_ROOT_DIR,
            'tools.staticfile.root'  : chatparam.OTS_ROOT_DIR,
            'tools.gzip.on'          : True,
            'tools.caching.on'       : False,
            'tools.sessions.timeout' : 300,
            'tools.sessions.on'      : True,
            'tools.session_auth.on'  : True,
            'tools.session_auth.login_screen' : root.login_page,
            'tools.session_auth.do_login' : root.dologin,
            'tools.sessions.locking' : 'explicit',
            'tools.session_auth.debug' : True,
            'request.error_response' : root.handle_error
            },
        '/css': {
            'tools.session_auth.on'  : False,
            'tools.staticdir.on'  : True,
            'tools.staticdir.dir' : 'css'
            },
        '/js': {
            'tools.session_auth.on'  : False,
            'tools.staticdir.on'  : True,
            'tools.staticdir.dir' : 'js'
            },
        '/img': {
            'tools.session_auth.on'  : False,
            'tools.staticdir.on'  : True,
            'tools.staticdir.dir' : 'img'
            },
        '/user/signup' : {
            'tools.sessions.on'        : False,
            'tools.session_auth.on'  : False,
            }
        }
    cherrypy.config.update(config['global'])
    app = cherrypy.tree.mount(root, config=config)
    try:
        dbm = dboperations.DBManager()
        dbm.init_db()
        __builtins__.chatDBManager = dbm

        apiserver = chatapiserver.APIServer()
        __builtins__.chatServer = apiserver

        print "Started chat successfully."
        cherrypy.engine.start()
        cherrypy.engine.block()
    except Exception, fault:
        print "Could not start chat. Error : ", str(fault)
        traceback.print_stack()
        
if __name__=="__main__":
    run()
