from db_conf import *

def _get_user_id(username):
    return redis_client.get(':'.join([USERNAME, username,  UID]))

def _get_user_name(uid):
    return redis_client.hget(':'.join([UID, uid, HASH]), USERNAME)

def _get_user_headimage(uid):
    return redis_client.hget(':'.join([UID, uid, HASH]), HEADIMAGE)

def _get_user_friends(uid):
    #TODO:
    pass

def _get_user_likes(uid):
    #TODO:
    pass
