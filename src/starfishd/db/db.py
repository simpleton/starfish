import json
import web
import redis
import db_video
import db_user
from db_conf import *


def new_user(username, head_image):
    if (redis_client.exists(':'.join([USERNAME,username,UID]))):
        #already in database
        return False
    else :
        userid = str(redis_client.incr(GLOBAL_USERID_FLAG))
        print ':'.join([USERNAME,username,UID])
        redis_client.set(':'.join([USERNAME, username,  UID]), userid)
        userinfo = {USERNAME:username, HEADIMAGE:head_image}
        redis_client.hmset(':'.join([UID, userid, HASH]), userinfo)
        return True

def get_user_base_info(username):
    return redis_client.get(':'.join([USERNAME, username,  UID]))

def check_user_exist_by_name(username):
    return redis_client.exists(':'.join([USERNAME,  username, UID]))

def _print_all_user():
    print redis_client.keys()

def new_video(owner, filepath, sha1):
    if (not redis_client.exists(':'.join([VIDEO_SHA1, sha1, VID]))):
        vid = str(redis_client.incr(GLOBAL_VIDEOID_FLAG))
        db_video._init_empty_video_info(vid)
        redis_client.set(':'.join([VIDEO_SHA1, sha1, VID]), vid)
        
        info = {VIDEO_SHA1:sha1, OWNER:owner, FILEPATH:filepath}
        redis_client.hmset(':'.join([VID, vid, HASH]), info)

        uid = db_user._get_user_id(owner)
        redis_client.lpush(':'.join([UID, uid, VIDEO_LIST]), vid)
        return True
    else:
        #already in database
        return False
        

def get_video_base_info(vid):
    baseinfo = redis_client.hgetall(':'.join([VID, vid, HASH]))
    return json.dumps(baseinfo)

def get_video_list_byuserid(uid):
    video_list = redis_client.lrange(':'.join([UID, uid, VIDEO_LIST]),0 ,-1)
    return video_list

def get_video_list_byusername(username):
    uid = db_user._get_user_id(username)
    vid_list = get_video_list_byuserid(uid)
    video_list = []
    for i in vid_list:
        video_list.append(get_video_base_info(i))
    mdict = {}
    #TODO:
    mdict['error_code'] = 'success'
    mdict['VIDEO_LIST'] = video_list
    mdict['total_size'] = len(vid_list)
    return json.dumps(mdict)
    
def _clear_all():
    for elem in redis_client.keys():
        redis_client.delete(elem)
    
if __name__ == '__main__':
    _clear_all()
    _print_all_user()
