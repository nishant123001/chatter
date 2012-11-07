import cherrypy
from chatpanel import render, render_page
from chatpanel.User import User
from chatpanel.Chat import Chat
from chatlib import authutil

class Root:
    """
        base handler
    """
    def __init__(self):
        self.user      = User()
        self.chat      = Chat()

    @cherrypy.expose
    def index(self, *args, **kwargs):
        raise cherrypy.HTTPRedirect('/chat/dashboard')

    @cherrypy.expose
    def login_page(self, from_page='/', username='', err_msg=''):
        #if cherrypy.session.get('username'):
         #   raise cherrypy.InternalRedirect('/dologout')
        context = {'page' : 'login.html', 'error' : err_msg}
        return render_page(context)

    def handle_error(self):
        content = ["""<html>
            <div align="left" style="color:red">Oops! An error occurred. Please check the logs for details.</div>
            </html>""" ]
        cherrypy.response.body = content

    @cherrypy.expose
    def dologin(self, username=None, password=None, from_page='', **kwargs):
        error = ''
        if not username:
            error += 'Please specify a username. \n'
        if not password:
            error = 'Please specify a password.'

        rc = chatServer.authenticate(username, password)
        if not rc["status"]:
            body = self.login_page(from_page, username, rc["error"])
            cherrypy.response.body = body
            if cherrypy.response.headers.has_key("Content-Length"):
                # Delete Content-Length header so finalize() recalcs it.
                del cherrypy.response.headers["Content-Length"]
            return True
        else:
            cherrypy.session['admin']   = rc["user"]
            cherrypy.session['username'] = cherrypy.request.login = username
            newurl = '/chat/dashboard'
            raise cherrypy.HTTPRedirect(newurl)

    @cherrypy.expose
    def dologout(self):
        cherrypy.session['username'] = ''
        cherrypy.lib.sessions.expire()  
        raise cherrypy.HTTPRedirect("/")



