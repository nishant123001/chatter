import sqlobject
import hashlib

from db import dbconnector
from sqlobject import SQLObject
from chatlib import chatparam

class User(sqlobject.SQLObject):
    name        =   sqlobject.UnicodeCol(length = 255, default = '')
    password    =   sqlobject.UnicodeCol(length = 255, default = '')
    
    def authenticate(self, pwd):
        authenticated =  pwd == self.password
        return authenticated

class Message(sqlobject.SQLObject):
    mthread         = sqlobject.ForeignKey('MThread')
    msgtext         = sqlobject.UnicodeCol()
    mfrom           = sqlobject.ForeignKey('User')
    mto             = sqlobject.ForeignKey('User')
    mtime           = sqlobject.IntCol()

class MThread(sqlobject.SQLObject):
    description     = sqlobject.UnicodeCol()
    updated         = sqlobject.IntCol()

class UserThdMap(sqlobject.SQLObject):
    user             = sqlobject.ForeignKey('User')
    thread           = sqlobject.ForeignKey('MThread')

class DBManager:
    def init_db(self):
        self.connectdb()
        self.init_tables()

    def connectdb(self):
        dbconnector.connectdb()

    def init_tables(self):
        User.createTable(ifNotExists =True)
        Message.createTable(ifNotExists = True)
        MThread.createTable(ifNotExists = True)
        UserThdMap.createTable(ifNotExists = True)
    
    def list_users(self):
        users = list(User.select())
        return users

    def create_user(self, params):
        return User(**params)

    def get_user(self, uname):
        user = User.selectBy(name = uname)
        user = user.getOne()
        return user

    def add_message(self, params):
        return Message(**params)

    def add_mthread(self, params):
        return MThread(**params)

    def map_user_thread(self, params):
        return UserThdMap(**params)

    def get_thread(self, threadid):
        return MThread.get(threadid)

    def get_mthread_messages(self, threadid):
        mthread = MThread.get(threadid)
        messages = Message.selectBy(mthread = threadid)
        return (mthread, messages)

    def list_mthreads(self, userid):
        mthreads = UserThdMap.selectBy(user=userid)
        return mthreads

    def update_mthread(self, threadid, utime):
        mthread = MThread.get(threadid)
        mthread.updated = utime
        return mthread

    def delete_mthread(self, threadid):
        connection = sqlobject.sqlhub.getConnection()
        transaction = connection.transaction()
        try:
            delete_query = transaction.sqlrepr(sqlbuilder.Delete(Message.sqlmeta.table, Message.q.mthread == threadid))
            transaction.query(delete_query)
            delete_query = transaction.sqlrepr(sqlbuilder.Delete(MThread.sqlmeta.table, MThread.q.id == threadid))
            transaction.query(delete_query)
        except Exception, fault:
            transaction.rollback()
            raise
        else:
            transaction.commit(close=True)
        return 

    def delete_message(self, messageid):
        msg = Message.get(messageid)
        msg.destroyself()

    def delete_tag(self, tagid):
        connection = sqlobject.sqlhub.getConnection()
        transaction = connection.transaction()
        transaction.sqlrepr(sqlbuilder.Delete(Question.sqlmeta.table, Question.q.tagid == tagid))
        transaction.sqlrepr(sqlbuilder.Delete(Tag.sqlmeta.table, Tag.q.id == tagid))
        transaction.commit(close=True)
        return
