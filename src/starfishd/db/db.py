import json
import web
import redis
import db_video
import db_user
from db_conf import *


def new_user(username, head_image):
    userid = str(redis_client.incr(GLOBAL_USERID_FLAG))
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

def new_video(owner, filepath, sha1):
    if (redis_client.exists(':'.join([VIDEO_SHA1, sha1, VID]))):
        #already in database
        return False
    else:
        videoid = str(redis_client.incr(GLOBAL_VIDEOID_FLAG))
        db_video._init_empty_video_info(videoid)
        redis_client.set(':'.join([VIDEO_SHA1, sha1, VID]), videoid)
        redis_client.hset(':'.join([VID, videoid, HASH]), VIDEO_SHA1, sha1)
        redis_client.hset(':'.join([VID, videoid, HASH]), OWNER, owner)
        redis_client.hset(':'.join([VID, videoid, HASH]), FILEPATH, filepath)
        return True
        

def get_video_base_info(vid):
    baseinfo = redis_client.hgetall(':'.join([VID, vid, HASH]))
    return json.dumps(baseinfo)

def _del_video(vid):
    sha1 = _get_video_sha1(vid)
    redis_client.delete(':'.join([VID, vid, HASH]))
    redis_client.delete(':'.join([VIDEO_SHA1, sha1, VID]))

def _clear_all():
    for elem in redis_client.keys():
        redis_client.delete(elem)
    
if __name__ == '__main__':
    #_clear_all()
    new_video('simsun','123','123')
    _print_all_user()
