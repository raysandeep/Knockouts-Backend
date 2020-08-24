from starlette.responses import HTMLResponse
from fastapi import FastAPI, Request, APIRouter
# from views.notif import Notifier
import requests as rq
import redis
import os

router = APIRouter()

# notifier = Notifier()

rs = redis.Redis.from_url(os.getenv("REDIS_URL"))

JUDGE_APIURL = os.getenv("JUDGEAPI_URL1")
BASE_URL = os.getenv("FASTAPI_URL")
DJANGO_URL = os.getenv("HOST_URL")

@router.on_event("startup")
async def startup_event():
    # await notifier.generator.asend(None)
    pass


@router.get("/api1")
async def get():
    return {}


@router.post("/api1/run")
async def runcode(req: Request):
    response = rq.request("POST", JUDGE_APIURL, json=await req.json())
    resp = response.json()
    print(type(resp))
    return resp


@router.get("/api1/trigger/{roomname}")
async def django(roomname):
    rs.set(roomname, "True")
    rs.expire(roomname, 60 * 2)
    return {}


@router.get("/api1/status/{roomname}")
async def docs(roomname):
    word = rs.get(roomname)
    rs.delete(roomname)
    return {word}
