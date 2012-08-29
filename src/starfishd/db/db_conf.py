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
POPULAR = 'is_hot'
PUBLIC = 'is_public'
OWNER = 'owner'
VIDEO_SHA1 = 'video_sha1'
HASH = 'hash'
URL = 'url'
PUBLIC_TIME = 'public_time'
VIDEO_LIST = 'video_list'
FOLLOWING_LIST = 'following_list'
FOLLOWER_LIST = 'follower_list'

LIKE_VIDEO_LIST = 'like_video_list'
LIKED_USER_LIST = 'liked_user_list'
redis_client = redis.Redis(host='127.0.0.1',port=6379, db=1)
