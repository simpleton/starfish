import json
import web
import redis

GLOBAL_ID_FLAG = 'Global:UserId'
USERNAME = 'username'
UID = 'uid'
HEADIMAGE = 'head_image'


redis_client = redis.Redis(host='127.0.0.1',port=6379, db=1)

def new_user(username, head_image):
    userid = str(redis_client.incr(GLOBAL_ID_FLAG))
    print 'add user id %d' , int(userid)
    print ':'.join([USERNAME,username,UID])
    if (redis_client.exists(':'.join([USERNAME,username,UID]))):
        #already in database
        return False
    else :
        redis_client.set(':'.join([USERNAME, username,  UID]), userid)
        redis_client.set(':'.join([UID, userid, USERNAME]), username)
        redis_client.set(':'.join([UID, userid, HEADIMAGE]), head_image)
        return True

def get_user_base_info(username):
    return redis_client.get(':'.join([USERNAME, username,  UID]))

def check_user_exist_by_name(username):
    return redis_client.exists(':'.join([USERNAME,  username, UID]))

def _print_all_user():
    print redis_client.keys()



if __name__ == '__main__':
    _print_all_user()
