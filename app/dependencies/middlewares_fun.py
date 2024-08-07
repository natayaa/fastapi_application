from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import Response, JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from itsdangerous import  URLSafeSerializer, BadSignature

import json

from time import time
from typing import List
from decouple import config

from .oauth2 import get_current_user

csrf_token_key = config("OAUTH2_CSRF_SECRET_KEY")
accepted_host = json.loads(config("ACCEPTED_HOST_CONTROL"))


class CSRFMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, secret_key=csrf_token_key, token_name="csrf_token", max_age=3600, excluded_path: list = None):
        super().__init__(app)
        self.secret_key = secret_key
        self.token_name = token_name
        self.max_age = max_age
        self.excluded_path = excluded_path or []
        self.serializer = URLSafeSerializer(self.secret_key)

    async def dispatch(self, request: Request, call_next):
        if request.url.path not in self.excluded_path and request.method in ["POST", "PUT", "DELETE", "PATCH"]:
            csrf_token = request.headers.get("X-CSRF-Token")
            if not csrf_token:
                return JSONResponse(content={"message": "Missing CSRF Token"})

            try:
                self.serializer.loads(csrf_token, max_age=self.max_age)
            except BadSignature:
                return JSONResponse(content={"message": "Invalid CSRF Token , Please reset/refresh the browser."})

        response = await call_next(request)
        
        if request.method == "GET":
            csrf_token = self.serializer.dumps({"csrf": "token"})
            response.set_cookie(self.token_name, csrf_token)
        
        return response
    


class AuthMiddleware(BaseHTTPMiddleware):
    """
        Globally search authorization on each avaliable endpoint except 
        for allowed_paths :)
    """
    def __init__(self, app, allowed_paths: List[str] = None):
        super().__init__(app)
        self.allowed_paths = allowed_paths or []

    async def dispatch(self, request: Request, call_next):
        if self.is_exempt_path(request) or self.is_localhost(request):
            return await call_next(request)

        try:
            user = await self.authenticate(request)
            request.state.user = user
        except HTTPException as e:
            return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
        except Exception as e:
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": "Internal Server Error"})

        return await call_next(request)

    def is_exempt_path(self, request: Request) -> bool:
        return request.url.path in self.allowed_paths

    def is_localhost(self, request: Request) -> bool:
        return request.client.host in ["127.0.0.1", "localhost"]

    async def authenticate(self, request: Request):
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            user = await get_current_user(token=token)
            if not user:
                return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content={"message": "Signature verification failed"})
            return user
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authenticated")

    def is_localhost(self, request: Request):
        # Check if the request is from localhost or a specific IP address
        host = request.client.host
        return host in accepted_host
    

class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, max_request: int, window_seconds: int):
        super().__init__(app)
        self.max_requests = max_request
        self.window_seconds = window_seconds
        self.requests = {}

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time()
        if client_ip not in self.requests:
            self.requests[client_ip] = []
        self.requests[client_ip] = [timestamp for timestamp in self.requests[client_ip] if current_time - timestamp < self.window_seconds]

        if len(self.requests[client_ip]) >= self.max_requests:
            return JSONResponse(status_code=status.HTTP_429_TOO_MANY_REQUESTS, content={"detail": "Too many request, please try again next time"})
        
        self.requests[client_ip].append(current_time)
        response = await call_next(request)
        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        # response.headers['Content-Security-Policy'] = 'default-src "self"'
        response.headers['X-Content-Type-Options'] = "nosniff"
        response.headers['X-Frame-Options'] = "DENY"
        response.headers['Strict-Transport-Security'] = "max-age=83457645736; includeSubDomains; preload"
        response.headers['X-XSS-Protection'] = "1; mode=block"
        return response