import cherrypy
import traceback
from chatpanel import render
from chatpanel import render, render_page, render_response
from chatlib import chatutil

class Chat:
    def __init__(self):
        pass

    @cherrypy.expose
    def index(self, *args, **kwargs):
        raise cherrypy.HTTPRedirect('/chat/dashboard')

    @cherrypy.expose
    def dashboard(self, *args, **kwargs):
        #import rpdb2
        #rpdb2.start_embedded_debugger('nky')
        users = chatServer.list_users(cherrypy.session['admin']["id"])
        mthreads = chatServer.list_threads(cherrypy.session['admin']["id"])
        messages = []
        replyto = ''
        selected = int(kwargs.get("selected", 0))
        for mthread in mthreads:
            if not selected:
                selected = mthread["id"]

            if selected == mthread["id"]:
                messages = chatServer.list_thread_messages(mthread["id"])["messages"]
                mthread['color'] = "antiquewhite"
            else:
                mthread['color'] = "aliceblue"

        if selected:
            display = ""
        else:
            display = "display:none"
        context = {"users"  : users,
                "msg"       : "",
                "threads"   : mthreads,
                "messages"  : messages,
                "threadid"  : selected,
                "display"   : display
                    }
        print context
        return render(context)
    
    @cherrypy.expose
    def goto_selected(self, *args, **kwargs):
        selected = kwargs.get('selected', 0)
        if selected:
            raise cherrypy.HTTPRedirect('/chat/dashboard?selected=%s'%selected)
        else:
            raise cherrypy.HTTPRedirect('/chat/dashboard')

    @cherrypy.expose
    def submit_reply(self, *args, **kwargs):
        chatServer.reply(cherrypy.session['admin']["id"], cherrypy.session['admin']["id"], kwargs["replymessage"], int(kwargs["mthreadid"]))
        raise cherrypy.HTTPRedirect('/chat/dashboard?selected=%d'%int(kwargs["mthreadid"]))
    
    @cherrypy.expose
    def submit_chat(self, *args, **kwargs):
        message = kwargs["message"]
        del kwargs["message"]
        receivers = []
        for elem in kwargs.keys():
            receivers.append(int(elem))

        chatServer.send_thread_msg(cherrypy.session['admin']["id"], receivers, message)
        raise cherrypy.HTTPRedirect('/chat/dashboard')
        

    
