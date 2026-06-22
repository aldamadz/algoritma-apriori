import asyncio
from http import HTTPStatus
from urllib.parse import unquote

from app.main import app
from app.db.base import Base
from app.db.session import engine

Base.metadata.create_all(bind=engine)


def _headers_from_environ(environ):
    headers = []
    for key, value in environ.items():
        if key.startswith("HTTP_"):
            name = key[5:].replace("_", "-").lower().encode("latin-1")
            headers.append((name, str(value).encode("latin-1")))
    if environ.get("CONTENT_TYPE"):
        headers.append((b"content-type", str(environ["CONTENT_TYPE"]).encode("latin-1")))
    if environ.get("CONTENT_LENGTH"):
        headers.append((b"content-length", str(environ["CONTENT_LENGTH"]).encode("latin-1")))
    return headers


def application(environ, start_response):
    method = environ.get("REQUEST_METHOD", "GET")
    path = unquote(environ.get("PATH_INFO") or "/")
    query_string = (environ.get("QUERY_STRING") or "").encode("latin-1")
    scheme = environ.get("wsgi.url_scheme", "http")
    server = (environ.get("SERVER_NAME") or "localhost", int(environ.get("SERVER_PORT") or 80))
    content_length = int(environ.get("CONTENT_LENGTH") or 0)
    body = environ["wsgi.input"].read(content_length) if content_length else b""

    scope = {
        "type": "http",
        "asgi": {"version": "3.0", "spec_version": "2.3"},
        "http_version": environ.get("SERVER_PROTOCOL", "HTTP/1.1").split("/")[-1],
        "method": method,
        "scheme": scheme,
        "path": path,
        "raw_path": path.encode("utf-8"),
        "query_string": query_string,
        "root_path": environ.get("SCRIPT_NAME", ""),
        "headers": _headers_from_environ(environ),
        "server": server,
        "client": (environ.get("REMOTE_ADDR") or "", int(environ.get("REMOTE_PORT") or 0)),
    }

    response = {"status": 500, "headers": [], "body": []}
    request_sent = False

    async def receive():
        nonlocal request_sent
        if not request_sent:
            request_sent = True
            return {"type": "http.request", "body": body, "more_body": False}
        await asyncio.sleep(0)
        return {"type": "http.disconnect"}

    async def send(message):
        if message["type"] == "http.response.start":
            response["status"] = message["status"]
            response["headers"] = message.get("headers", [])
        elif message["type"] == "http.response.body":
            response["body"].append(message.get("body", b""))

    asyncio.run(app(scope, receive, send))

    status_code = int(response["status"])
    phrase = HTTPStatus(status_code).phrase if status_code in HTTPStatus._value2member_map_ else "OK"
    status_line = f"{status_code} {phrase}"
    headers = [(k.decode("latin-1"), v.decode("latin-1")) for k, v in response["headers"]]
    start_response(status_line, headers)
    return response["body"]
