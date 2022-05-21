from time import sleep
from itsdangerous import URLSafeTimedSerializer
s = URLSafeTimedSerializer("secret")
token = s.dumps({"user_id":1})
print(token)

# using max_age in loads will raise error if time passed more than the max age that is the expiration period
print(s.loads(token,max_age=2))
sleep(3) # sleeping for 2sec
print(s.loads(token,max_age=2)) # error as expiration set to 2s and sleeping for more than 2s