import sqlobject
from sqlobject.sqlite import builder
from chatpanel import chatparam
from sqlobject.sqlite import sqliteconnection
class DBConnection(sqliteconnection.SQLiteConnection):
    pass

def connectdb():
    try:
        print 'dbfile', chatparam.OTS_DB_FULLNAME
        connection = DBConnection(chatparam.OTS_DB_FULLNAME)
        sqlobject.sqlhub.processConnection = connection
        print "Connection established. ", connection
    except Exception, fault:
        raise Exception("Connect db failed. Error %s" % str(fault))
