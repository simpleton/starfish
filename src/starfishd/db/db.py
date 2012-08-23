import json
import web
import redis

GLOBAL_USERID_FLAG = 'Global:UserId'
USERNAME = 'username'
UID = 'uid'
HEADIMAGE = 'head_image'

GLOBAL_VIDEOID_FLAG = 'Global:VideoId'
VID = 'vid'

LOCALE = 'locale'
POPULAR = 'popular'
TITLE = 'title'
SPOT = 'spot'
POPULAR = 'popular'
PUBLIC = 'public'
OWNER = 'owner'
VIDEO_SHA1 = 'video_sha1'
FILEPATH = 'filepath'
HASH = 'hash'
URL = 'url'

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

def new_video(owner, filepath, sha1):
    if (redis_client.exists(':'.join([VIDEO_SHA1, sha1, VID]))):
        #already in database
        return False
    else:
        videoid = str(redis_client.incr(GLOBAL_VIDEOID_FLAG))
        _init_empty_video_info(videoid)
        redis_client.set(':'.join([VIDEO_SHA1, sha1, VID]), videoid)
        redis_client.hset(':'.join([VID, videoid, HASH]), VIDEO_SHA1, sha1)
        redis_client.hset(':'.join([VID, videoid, HASH]), OWNER, owner)
        redis_client.hset(':'.join([VID, videoid, HASH]), FILEPATH, filepath)
        return True
        
def _init_empty_video_info(vid):
    item = {SPOT:'', POPULAR:'', TITLE:'', PUBLIC:'', URL:'', VIDEO_SHA1:'', OWNER:'', VID:''}
    redis_client.hmset(':'.join([VID, vid, HASH]), item)
    
    
def _set_video_title(vid, title):
    if (redis_client.exists(':'.join([VID, vid , HASH]))):
        redis_client.hset(':'.join([VID, vid, HASH]), TITLE, title)

def _set_video_spot(vid, vspot):
    if (redis_client.exists(':'.join([VID, vid, HASH]))):
        redis_client.hset(':'.join([VID, vid, HASH]), SPOT, vspot)

def _set_video_popular(vid , popular):
    if (redis_client.exists(':'.join([VID, vid , HASH]))):
        redis_client.hset(':'.join([VID, vid, HASH]), POPULAR, popular)

def _set_video_public(vid , authority):
    if (redis_client.exists(':'.join([VID, vid , HASH]))):
        #TODO: user check
        redis_client.hset(':'.join([VID, vid, HASH]), PUBLIC, authority)

def _get_video_title(vid):
    return redis_client.hget(':'.join([VID, vid, HASH]), TITLE)
    
def _get_video_spot(vid):
    return redis_client.hget(':'.join([VID, vid, HASH]), SPOT)

def _get_video_POPULAR(vid):
    return redis_client.hget(':'.join([VID, vid, HASH]), POPULAR)

def _get_video_public(vid):
    return redis_client.hget(':'.join([VID, vid, HASH]), PUBLIC)

def _get_video_url(vid):
    #TODO: implement me
    return 'www.soso.com'

def _get_video_owner(vid):
    return redis_client.hget(':'.join([VID, vid, HASH]), OWNER)

def _get_video_id(sha1):
    return redis_client.get(':'.join([VIDEO_SHA1, sha1, VID]))

def _get_video_sha1(vid):
    return redis_client.hget(':'.join([VID, vid, HASH]), VIDEO_SHA1)

def get_video_base_info(vid):
    """    baseinfo = {}
    baseinfo['id'] = vid
    baseinfo['title'] = _get_video_title(vid)
    baseinfo['spot'] = _get_video_spot(vid)
    baseinfo['is_hot'] = _get_video_POPULAR(vid)
    baseinfo['is_public'] = _get_video_public(vid)
    baseinfo['url'] = _get_video_url(vid)
    baseinfo['owner'] = _get_video_owner(vid)
    return json.dumps(baseinfo) """
    baseinfo = redis_client.hgetall(':'.join([VID, vid, HASH]))
    return json.dumps(baseinfo)


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

def _del_video(vid):
    sha1 = _get_video_sha1(vid)
    redis_client.delete(':'.join([VID, vid, HASH]))
    redis_client.delete(':'.join([VIDEO_SHA1, sha1, VID]))

def _clear_all():
    for elem in redis_client.keys():
        redis_client.delete(elem)
    
if __name__ == '__main__':
    #_clear_all()
    _print_all_user()
