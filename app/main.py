from fastapi import FastAPI, status, HTTPException, Request
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.security.oauth2 import OAuth2AuthorizationCodeBearer
from fastapi.exception_handlers import http_exception_handler
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


import uvicorn, logging
from loguru import logger
from decouple import config
from datetime import datetime

from dependencies.middlewares_fun import CSRFMiddleware, AuthMiddleware, RateLimitMiddleware, SecurityHeadersMiddleware
from routes.include.const_logger import InterceptHandler, configure_logger

from routes.v1.redirect import incident_handler
from routes.v1.upload_file import upload_file
from routes.v1.users import user_section
from routes.v1.telebot import tele_bot_client

# logger
from routes.v1.ext.loggerClass import ProtocolLoggers, logfileHandlers


endpoints_app = FastAPI(
    title=config("APPLICATION_TITLE"),
    version=config("APPLICATION_VERSION"),
    description="Something you need to know that this shit are completely different",
    debug=bool(config("APPLICATION_DEBUG"))
)
# logger worker
logdir = "./files/var/logs/"

"""@endpoints_app.middleware("http")
async def log_app(request: Request, call_next):
    current_Time = datetime.now().strftime("%Y-%m-%d-%H:%M")
    response = await call_next(request)
    if logging.getLogger("uvicorn.access"):
        log_dt = ProtocolLoggers(loglevel="info", logfile=logdir + f"/info/access_{current_Time}.log", logger_="uvicorn.access")
        log_dt.conf_log()
    elif logging.getLogger("uvicorn.error"):
        log_dt = ProtocolLoggers(loglevel="error", logfile=logdir + f"/error/access_fail_{current_Time}.log", logger_="uvicorn.error")
        log_dt.conf_log()
    return response"""


#configure_logger()


# disable atm 
#endpoints_app.add_middleware(CSRFMiddleware, excluded_path=["/", "/docs", "/openapi.json"])
#endpoints_app.add_middleware(RateLimitMiddleware, max_request=5, window_seconds=60)
endpoints_app.add_middleware(AuthMiddleware, allowed_paths=list(config("EXCLUDED_ENDPOINT_PATH", default=",")))
endpoints_app.add_middleware(SecurityHeadersMiddleware)
endpoints_app.add_middleware(CORSMiddleware, allow_origins=config("APPLICATION_CLIENT_ORIGIN").split(","), allow_credentials=True, allow_methods=["GET", "POST", "PUT", "DELETE"], allow_headers=["*"])

endpoints_app.include_router(incident_handler, include_in_schema=True)
endpoints_app.include_router(upload_file, include_in_schema=True)
endpoints_app.include_router(user_section)
endpoints_app.include_router(tele_bot_client)


if __name__ == '__main__':
    uvicorn.run(app="main:endpoints_app", host=config("HOST_SERVER_CONTROL"), port=int(config("HOST_SERVER_PORT")), 
                reload=True)