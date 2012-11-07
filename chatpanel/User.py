import cherrypy
import traceback
from chatpanel import render
from chatpanel import render, render_page, render_response
from chatlib import chatutil

class User:
    def __init__(self):
        pass
    
    @cherrypy.expose
    def signup(self, *args, **kwargs):
        try:
            print kwargs
            error = None
            context = {}
            name        = kwargs['username']
            password    = kwargs['password']
            cpassword    = kwargs['cpassword']
            
            if not name:
                error = "Please specify an name"
            if cpassword <> password:
                error  = "Password and confirm password do not match"

            if error :
                context.update({'error' : error, 'page': 'login.html'})
                return render_page(context)

            user = chatServer.create_user({"name" : name, "password": password})

            context.update({'page' : 'login.html',
                            'error'        : 'User sucessfully created for %s'%user['name']
                       })
            return render_page(context)
        except Exception, fault:
            raise
