import json
import web
import redis

GLOBAL_USERID_FLAG = 'Global:UserId'
USERNAME = 'username'
UID = 'uid'
HEADIMAGE = 'head_image'

GLOBAL_VIDEOID_FLAG = 'Global:VideoId'
VID = 'vid'
VIDEO_TITLE = 'video_title'
LOCALE = 'locale'
POPULAR = 'popular'


redis_client = redis.Redis(host='127.0.0.1',port=6379, db=1)

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

def new_video(owner, filepath, SHA1):
    videoid = str(redis_client.incr(GLOBAL_VIDEOID_FLAG))
    print 'add video id %s' , videoid
    if (redis_client.exists(':'.join([VIDEO_SHA1, SHA1, VID]))):
        #already in database
        return False
    else:
        redis_client.set(':'.join([VIDEO_SHA1, SHA1, VID]), videoid)
        redis_client.set(':'.join([VID, videoid, VIDEO_SHA1]), SHA1)
        redis_client.set(':'.join([VID, videoid, OWNER]), owner)
        redis_client.set(':'.join([VID, videoid, FILEPATH]), filepath)
        


if __name__ == '__main__':
    _print_all_user()
