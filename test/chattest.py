import os
import time
from chatlib import chatparam
from db import dboperations
from chatlib import chatapiserver

def create_user(username, password):
    wrongpassword = "wrongpassword"
    user    = chatServer.create_user({"name" : username, "password": password})
    if not user["name"] == username:
        raise Exception("Error createing user")

    ret = chatServer.authenticate(username, wrongpassword)
    if ret["status"]:
        raise Exception("Wrong password acceptd")

    ret = chatServer.authenticate(username, password)
    if not ret["status"]:
        raise Exception("Correct password not accepted")

    return ret["user"]

def list_users(user):
    ret = chatServer.list_users(user["id"])
    if len(ret) <> 2:
        raise Exception("Incorrect number of users returned in user_count")
    if debug:
        print "List for user %s returned : %s"%(user, ret)
    return ret

def start_msg_thread(sender, receivers, msg):
    msgto = []
    for receiver in receivers:
        msgto.append(receiver["id"])
    chatServer.send_thread_msg(sender["id"], msgto, msg)

def check_threads(user):
    ret = chatServer.list_threads(user["id"])
    if len(ret) <> 2:
        raise Exception("Incorrect number of theads")

    if debug:
        print "check threads for user %s returned : %s"%(user, ret)

    return ret

def reply_thread(mfrom, mto, msg, mthread):
    chatServer.reply(mfrom["id"], mto["id"], msg, mthread["id"])

def check_thread_messages(mthread):
    print "\n Check thread messages \n"
    ret = chatServer.list_thread_messages(mthread["id"])
    if len(ret["messages"]) <> 2:
        raise Exception("Incorrect number of messages")

    if debug:
        print "messages in thread %s returned : %s"%(mthread, ret)

if __name__ == "__main__":
    # delete previous db every time you run the test
    chatparam.OTS_DB_FULLNAME     = os.path.join(chatparam.OTS_DB_PATH, 'Test%d.db'%(int(time.time())))
    try:
        os.remove(chatparam.OTS_DB_FULLNAME)
    except Exception, fault:
        print str(fault)

    dbm = dboperations.DBManager()
    dbm.init_db()
    __builtins__.chatDB = dbm

    apiserver = chatapiserver.APIServer()
    __builtins__.chatServer = apiserver

    __builtins__.debug = True

    username1       = "user1"
    password1       = "password1"
    username2       = "user2"
    password2       = "password2"
    username3       = "user3"
    password3       = "password3"
    msg1            = "first message Hi nishant this is my "
    replymsg1       = "Hi dude it works first time"
    msg2            = "second messageHi nishant this is my"
    replymsg2       = "Hi dude it works second time"

    #import rpdb2
    #rpdb2.start_embedded_debugger("nky")
    user1 = create_user(username1, password1)
    user2 = create_user(username2, password2)
    user3 = create_user(username3, password3)
    
    ulist = list_users(user1)

    start_msg_thread(user1, [user2, user3], msg1)
    start_msg_thread(user2, [user1, user3], msg2)

    threads = check_threads(user3)

    reply_thread(user3, user2, replymsg1, threads[0])
    check_thread_messages(threads[0])

