import json
import web
import redis

redis_client = redis.Redis(host='127.0.0.1',port=6379, db=1)

def new_user(id, nick_name, head_image):
    d = {}
    d['id'] = id
    d['nick'] = nick_name
    d['head_image'] = head_image
    json_obj = json.dumps(d)
    redis_client.set(id, json_obj)
    
def get_user_base_info(UID):
    return redis_client.get(UID)

if __name__ == "__main__":
    new_user('1', 'hello', 'http://www.baidu.com')
    print redis_client.get('1')
