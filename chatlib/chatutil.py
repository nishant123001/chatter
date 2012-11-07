import copy
import types
from chatlib import chatparam
import sqlobject

def encrypt(str):
    return 'chat' + str

def decrypt(str):
    return str[3:]

def obj2dic(obj):

    if not isinstance(obj, sqlobject.SQLObject):
        return {}

    ret = {}
    if not hasattr(obj, '__dict__'):
        return {}

    for k in obj.__dict__.keys():
        if k.startswith('_SO_val_'):
            k = k.split('_SO_val_')[1]
            if k.endswith('ID') and len(k) > 2:
                fk = k[:-2]
                ret[fk] = getattr(obj, k)
                continue
            ret[k] = getattr(obj, k)

            # MySQL returns a long for all integers. Convert smaller than
            # 2G to int.
            if isinstance(ret[k], types.LongType):
                ret[k] = int(ret[k])
    ret['id'] = obj.id
    return ret

def questionOptionlDetails(options):
    quedetails = copy.deepcopy(chatparam.QUESTION_OPTIONAL_DETAILS)
    quedetails['numoptions']    = len(options)
    quedetails['options']       = options
    return quedetails
   
# Note here is just a special instruction if any to be put under that question
def questionOptionlDetails(note):
    quedetails = copy.deepcopy(chatparam.QUESTION_SUBJECTIVE_DETAILS)
    quedetails['note']    = note
    return quedetails
