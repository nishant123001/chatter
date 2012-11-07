import os

def get_root_dir():
    cwd = os.getcwd()
    return cwd

OTS_ROOT_DIR        = get_root_dir()
OTS_BASE_TEMPLATE   = 'base.html'
OTS_PROJECT_NAME    = 'Chatter'
OTS_DB_PATH         = get_root_dir()
OTS_DB_NAME         = 'otsconfig.db'
OTS_DB_TEST_NAME    = 'otsconfig_test%d.db'
OTS_DB_FULLNAME     = os.path.join(OTS_DB_PATH, OTS_DB_NAME)

OTS_HOST_PORT        = 8001
OTS_HOST_HREF        = 'http://127.0.0.1:' + str(OTS_HOST_PORT)

# SMTP RELATED SETTINGS
SMTP_HOSTNAME       = 'smtp.gmail.com'
SMTP_PORT           = 25
SMTP_USERNAME       = 'ots1510@gmail.com'
SMTP_PASSWORD       = 'amitnishantprahladprince'
SMTP_TLS            = True

# MAIL
DEFAULT_SENDER_EMAILID = 'ots1510@gmail.com'

# Question Types
MULTIPLE_CHOICE_TYPE_QUESTION    = 1
SUBJECTIVE_TYPE_QUESTION         = 2
CODING_TYPE_QUESTION             = 3

# Question details
# Always use copy.deepcopy
QUESTION_OPTIONAL_DETAILS = {
        'numoptions'    : 0,
        'options'       : []
        }

QUESTION_SUBJECTIVE_DETAILS = {
        'note'    : '',
        }

OTS_SECRET = 'qaw1zs2xe3dr8cf4va9ws2zsx6edr9cfv11tgy55bh77nehs'

RETURN_SUCCESS = 'OK'
