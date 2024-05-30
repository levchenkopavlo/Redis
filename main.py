import redis

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

r.set('user:name', 'Alice')
name = r.get('user:name')
print(name)
