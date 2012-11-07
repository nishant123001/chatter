from sqlobject import SQLObjectNotFound
from chatlib import chatutil
from chatlib import chatparam

import time

"""
apiserver should be the only point where type conversions should take place.
e.g. webpanel should not worry about pickle loading the question details.
 for adding questions, let webpanel send dict and apiserver will convert to pickle before saving and
 convert to dict when fetching
"""

class UserAPI:
    def create_user(self, params):
        rc = chatutil.obj2dic(chatDBManager.create_user(params))
        del rc["password"]
        return rc 

    def authenticate(self, username, password):
        ret = {"status": 1, "error": "", "user": {}}
        try:
            error = None
            user_obj = chatDBManager.get_user(username)
            authenticated = user_obj.authenticate(password)
            user_dict = chatutil.obj2dic(user_obj)
            del user_dict["password"]
            ret["user"] = user_dict
            if not authenticated:
                ret["status"] = 0
                ret["error"] = "invalid password"
        except SQLObjectNotFound:
            ret["status"] = 0
            ret["error"] = "invalid username"
        except Exception, fault:
            ret["status"] = 0
            ret["error"] = str(fault)
        return ret

    def list_users(self, userid):
        ulist = chatDBManager.list_users()
        ret = []
        for uobj in ulist:
            if uobj.id == userid:
                pass
            else:
                user_dict =chatutil.obj2dic(uobj) 
                del user_dict["password"]
                ret.append(user_dict)
        return ret

class ChatAPI:

    def send_thread_msg(self, sender, uids, msg):
        curr_time = int(time.time())
        params = {"description" : msg[:10] + "...", "updated" : curr_time}
        mparams = {"msgtext": msg, "mfrom": sender, "mtime": curr_time}

        for uid in uids:
            mthread = chatDBManager.add_mthread(params)
            chatDBManager.map_user_thread({"user": uid, "thread": mthread.id})
            chatDBManager.map_user_thread({"user": sender, "thread": mthread.id})

            mparams["mthread"] = mthread.id
            mparams["mto"] = uid
            chatDBManager.add_message(mparams)
        return

    def reply(self, mfrom, mto, msg, mthread):
        curr_time = int(time.time())
        params = {"msgtext": msg, "mfrom": mfrom, "mtime": curr_time, "mto": mto, "mthread": mthread}
        chatDBManager.add_message(params)
        chatDBManager.update_mthread(mthread, curr_time)
        return 

    def list_thread_messages(self, threadid):
        ret = {"updated": 0, "messages": [], "description" : ''}
        mthread, messages = chatDBManager.get_mthread_messages(threadid)
        ret["updated"] = mthread.updated
        ret["description"] = mthread.description
        messages = list(messages)
        messages.sort(key = lambda x: x.mtime)

        for message in messages:
            msg_dict = chatutil.obj2dic(message)
            msg_dict['mtime'] = time.strftime("%m/%d/%Y %I:%M %p",time.localtime(msg_dict['mtime']))
            msg_dict['from'] =  message.mfrom.name
            ret["messages"].append(msg_dict)
        return ret

    def list_threads(self, uid):
        ret = []
        mthreads = chatDBManager.list_mthreads(uid)
        for mthread in mthreads:
            thread = chatutil.obj2dic(chatDBManager.get_thread(mthread.threadID))
            thread['updated'] = time.strftime("%m/%d/%Y %I:%M %p",time.localtime(thread['updated'])) 
            ret.append(thread)
        ret.sort(cmp = lambda x,y : cmp(y, x), key = lambda x: x["updated"])
        return ret

class APIServer(UserAPI, ChatAPI):
    pass
