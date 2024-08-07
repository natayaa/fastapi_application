from fastapi import APIRouter, Request, status



admin_endpoint = APIRouter("/application/version/v1", tags=['Administrator Endpoint'])

#@admin_endpoint.get("")