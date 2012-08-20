import json
import web
import redis

redis_client = redis.Redis(host='127.0.0.1',port=6379, db=1)

def new_user(uid, nick_name, head_image):
    d = {}
    d['id'] = uid
    d['nick'] = nick_name
    d['head_image'] = head_image
    json_obj = json.dumps(d)
    redis_client.set(uid, json_obj)
    
def get_user_base_info(uid):
    return redis_client.get(uid)

def check_user_exist(uid):
    return redis_client.exists(uid)

def _print_all_user():
    print redis_client.keys()
    
if __name__ == "__main__":
    _print_all_user()
