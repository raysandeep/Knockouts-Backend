  
from typing import List
from starlette.responses import HTMLResponse
from starlette.websockets import WebSocket, WebSocketDisconnect
from fastapi import FastAPI, Request, Depends,Response, HTTPException, status, APIRouter
from fastapi.responses import JSONResponse
import logging
from core import settings
from views.notif import Notifier
import json
import requests as rq
from urllib.parse import urlencode
import redis
import asyncio
from starlette.background import BackgroundTask

router = APIRouter()

notifier = Notifier()

rs = redis.Redis.from_url( 'redis://h:p2c7b86fd6dddcfc05382c802f75c05d84647fc3d818ca978154401849ab6aa13@ec2-54-208-37-185.compute-1.amazonaws.com:14339' )


JUDGE_APIURL = "http://15.207.88.35/submissions?base64_encoded=true&wait=true"
BASE_URL = "https://socketcompiler.herokuapp.com/"
DJANGO_URL = "https://competitive-edge.herokuapp.com/"
html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Compiler</title>
    </head>
    <body>
        <h1>WebSocket Code Excutions</h1>
        <p><b>Example:</b><br>
            {
                "submissions": [
                    {
                        "language_id": 71,
                        "source_code": "import pandas",
                        "stdin": "Hello world"
                    },
                    {
                        "language_id": 71,
                        "source_code": "a = 1\nif (a == 1):\n    print(\"okay\")",
                        "stdin": "Hello world"
                    }
                ]
            }<br>
            Make sure you url encode the whole souce code string before passing.<br>
            <b>Languages:</b><br>
            [{"id":45,"name":"Assembly (NASM 2.14.02)"},{"id":46,"name":"Bash (5.0.0)"},{"id":47,"name":"Basic (FBC 1.07.1)"},{"id":75,"name":"C (Clang 7.0.1)"},{"id":76,"name":"C++ (Clang 7.0.1)"},{"id":48,"name":"C (GCC 7.4.0)"},{"id":52,"name":"C++ (GCC 7.4.0)"},{"id":49,"name":"C (GCC 8.3.0)"},{"id":53,"name":"C++ (GCC 8.3.0)"},{"id":50,"name":"C (GCC 9.2.0)"},{"id":54,"name":"C++ (GCC 9.2.0)"},{"id":86,"name":"Clojure (1.10.1)"},{"id":51,"name":"C# (Mono 6.6.0.161)"},{"id":77,"name":"COBOL (GnuCOBOL 2.2)"},{"id":55,"name":"Common Lisp (SBCL 2.0.0)"},{"id":56,"name":"D (DMD 2.089.1)"},{"id":57,"name":"Elixir (1.9.4)"},{"id":58,"name":"Erlang (OTP 22.2)"},{"id":44,"name":"Executable"},{"id":87,"name":"F# (.NET Core SDK 3.1.202)"},{"id":59,"name":"Fortran (GFortran 9.2.0)"},{"id":60,"name":"Go (1.13.5)"},{"id":88,"name":"Groovy (3.0.3)"},{"id":61,"name":"Haskell (GHC 8.8.1)"},{"id":62,"name":"Java (OpenJDK 13.0.1)"},{"id":63,"name":"JavaScript (Node.js 12.14.0)"},{"id":78,"name":"Kotlin (1.3.70)"},{"id":64,"name":"Lua (5.3.5)"},{"id":79,"name":"Objective-C (Clang 7.0.1)"},{"id":65,"name":"OCaml (4.09.0)"},{"id":66,"name":"Octave (5.1.0)"},{"id":67,"name":"Pascal (FPC 3.0.4)"},{"id":85,"name":"Perl (5.28.1)"},{"id":68,"name":"PHP (7.4.1)"},{"id":43,"name":"Plain Text"},{"id":69,"name":"Prolog (GNU Prolog 1.4.5)"},{"id":70,"name":"Python (2.7.17)"},{"id":71,"name":"Python (3.8.1)"},{"id":80,"name":"R (4.0.0)"},{"id":72,"name":"Ruby (2.7.0)"},{"id":73,"name":"Rust (1.40.0)"},{"id":81,"name":"Scala (2.13.2)"},{"id":82,"name":"SQL (SQLite 3.27.2)"},{"id":83,"name":"Swift (5.2.3)"},{"id":74,"name":"TypeScript (3.7.4)"},{"id":84,"name":"Visual Basic.Net (vbnc 0.0.0.5943)"}]
            </p>
        <form action="" onsubmit="sendMessage(event)">
            <textarea name="" id="messageText" cols="100" rows="20"></textarea>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("wss://socketcompiler.herokuapp.com/ws/abc");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
            ws.onclose = function(){
                console.log("Socket Closed");
            }
            setTimeout(function() { console.log("Ending Socket"); ws.close(); }, 5000);
        </script>
    </body>
</html>
"""

SUBMISSION_URL = "http://13.233.147.80/submissions/batch"


@router.on_event("startup")
async def startup_event():
    await notifier.generator.asend(None)



@router.get("/")
async def get():
    return HTMLResponse(html)


@router.post("/run")
async def runcode(req: Request):
    response = rq.request("POST",JUDGE_APIURL,json=await req.json())
    resp = response.json()
    print(type(resp))
    return resp


@router.get("/trigger/{roomname}")
async def django(roomname):
    rs.set(roomname,"True")
    rs.expire(roomname,60*2)
    return {}


@router.get("/status/{roomname}")
async def docs(roomname):
    word = rs.get(roomname)
    rs.delete(roomname)
    return {word}

# docker build -t socketcompiler . 
# heroku container:push web -a socketcompiler
# heroku container:release web -a socketcompiler