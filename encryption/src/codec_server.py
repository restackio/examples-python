from collections.abc import Awaitable, Callable, Iterable
from functools import partial

from aiohttp import hdrs, web
from google.protobuf import json_format
from restack_ai.security import Payload, Payloads

from .codec import EncryptionCodec


def build_codec_server() -> web.Application:
    # Cors handler
    async def cors_options(req: web.Request) -> web.Response:
        resp = web.Response()
        if req.headers.get(hdrs.ORIGIN) == "http://localhost:8233":
            resp.headers[hdrs.ACCESS_CONTROL_ALLOW_ORIGIN] = "http://localhost:8233"
            resp.headers[hdrs.ACCESS_CONTROL_ALLOW_METHODS] = "POST"
            resp.headers[hdrs.ACCESS_CONTROL_ALLOW_HEADERS] = "content-type,x-namespace"
        return resp

    # General purpose payloads-to-payloads
    async def apply(
        fn: Callable[[Iterable[Payload]], Awaitable[list[Payload]]],
        req: web.Request,
    ) -> web.Response:
        # Read payloads as JSON
        if req.content_type != "application/json":
            raise web.HTTPUnsupportedMediaType(
                text="Only application/json is supported",
            )
        payloads = json_format.Parse(await req.read(), Payloads())

        # Apply
        payloads = Payloads(payloads=await fn(payloads.payloads))

        # Apply CORS and return JSON
        resp = await cors_options(req)
        resp.content_type = "application/json"
        resp.text = json_format.MessageToJson(payloads)
        return resp

    # Build app
    codec = EncryptionCodec()
    app = web.Application()
    app.add_routes(
        [
            web.post("/encode", partial(apply, codec.encode)),
            web.post("/decode", partial(apply, codec.decode)),
            web.options("/decode", cors_options),
        ],
    )
    return app


def run_codec_server() -> None:
    web.run_app(build_codec_server(), host="127.0.0.1", port=8081)
