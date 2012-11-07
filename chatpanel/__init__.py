import os
import cherrypy
import json
from genshi.template import TemplateLoader
from genshi.template import Context
from chatlib import chatparam

templates = None
loader = None

def initloader(chatdir):
    global templates, loader
    templates = os.path.join(chatdir, 'html')
    loader = TemplateLoader(templates, auto_reload=True)

def render(context_dict, base = chatparam.OTS_BASE_TEMPLATE):
    context_dict.setdefault('project_name', chatparam.OTS_PROJECT_NAME)
    username = 'Guest'
    try:
        username = cherrypy.session.get('username')
        context_dict.setdefault('username', username)
    except Exception, fault:
        pass
    ctx     = Context(**context_dict)
    tmpl    = loader.load(base)
    stream  = tmpl.generate(ctx)
    cherrypy.request.headers['Accept-Charset'] = 'utf-8;q=0.7,*;q=0.7'
    return stream.render('html', encoding='utf-8') 

def render_page(context_dict):
    return render(context_dict, context_dict['page'])
        
def render_response(rc):
    """
        return rc dict as JSON
    """
    rc = json.loads(rc)
    cherrypy.response.headers['Content-Type'] = 'application/json'
    return rc

"""
    TODO
    - as_json() and as_dict() are to be used only when running in "testing mode"
    - when not running in testing mode, these methods should not do anything.
    - later day optimization

"""
def as_json(rc):
    rc =  json.dumps(rc)
    return rc

def as_dict(rc):
    rc = json.loads(rc)
    return rc
