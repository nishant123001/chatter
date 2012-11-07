import cherrypy

def authenticate(username, password):
    """
    Moving the real authentication part to apiserver.
    Noreason, we should make a user object here and then fire authenticate on it.
    """

    return chatServer.authenticate(username, password)

def update_session(username):
    admin_obj                       = chatServer.get_admin_by_email(username)
    cherrypy.session['admin']       = admin_obj
    cherrypy.session['username']    = cherrypy.request.login = username
    cherrypy.session['customerid']  = admin_obj['customerid']


