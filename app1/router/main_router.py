from fastapi import APIRouter
from views import accounts


api_router = APIRouter()

api_router.include_router(accounts.router, tags=["login"])

