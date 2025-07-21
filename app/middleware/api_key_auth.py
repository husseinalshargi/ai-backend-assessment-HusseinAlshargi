from datetime import datetime, timezone
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

import app.database as db
from app.models.api_keys_record import APIKey
from app.scripts.rate_limiter import rate_limit




#create a middleware class in order to include in the api instance, this is a simpler approach
#for referance
#https://stackoverflow.com/questions/71525132/how-to-write-a-custom-fastapi-middleware-class

class APIKeyMiddleware(BaseHTTPMiddleware): 
    async def dispatch(self, request: Request, call_next):
        session = None
        response = None
        #here we will check if an admin is using the request to include his use only
        if request.url.path.startswith("/api/admin"):
            key = request.headers.get("X-API-Key") #header to ask for an api key
            if not key:
                return JSONResponse(status_code=401, content={"detail":"Missing API key"}) #if the user did not include the api key

            session = db.sessionlocal()
            try:
                api_key = session.query(APIKey).filter_by(key=key, active=True).first() #search for the key in the db
                if not api_key: #if it is not there or it's not associated to an admin
                    return JSONResponse(status_code=403, content={"detail": "Forbidden"})
                if api_key.role != "admin":
                    return JSONResponse(status_code=403, content={"detail": "Forbidden"})

                if not rate_limit(key):
                    return JSONResponse(status_code=429, content={"detail":"Rate limit exceeded"})

                # Update last used timestamp
                api_key.last_used_at = datetime.now(timezone.utc)
                session.commit()

            except Exception as e:
                print(f"[Middleware Error]: {e}")
                return JSONResponse(status_code=403, content={"detail": "Forbidden"})  # instead of 500
            finally:
                session.close()


        #process the request and get the response from it
        response = await call_next(request)

        if session:
            session.close()

        return response

