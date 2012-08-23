from db_conf import *

def _get_user_id(user_name):
    return redis_client.get(':'.join([USERNAME, username,  UID]))

def _get_user_name(uid):
    return redis_client.get(':'.join([UID, uid, USERNAME]))

def _get_user_headimage(uid):
    return redis_client.get(':'.join([UID, uid, HEADIMAGE]))

def _get_user_friends(uid):
    #TODO:
    pass

def _get_user_likes(uid):
    #TODO:
    pass
