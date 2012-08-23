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
