from app.database import r
import time


#limit rate using redis
def rate_limit(api_key: str, rate: int = 5, interval: int = 60): #5 requests for every 60 seconds
    key = f"rate_limit:{api_key}"

    tokens = r.get(key)
    if tokens is None: #it means it expired (time limit)
        r.set(key, rate - 1, ex=interval) #make the set expier after 60 sec (default)
        return True
    else:
        tokens = int(tokens) #convert from byte to an int
        if tokens > 0:
            r.decr(key) #make ie less by one
            return True #allow the use
        else:
            return False #less than 1 so do not allow