import json
import asyncio

from quart import Blueprint, Response, current_app, render_template, request, stream_with_context, make_response, jsonify

bp = Blueprint("chat", __name__, template_folder="templates", static_folder="static")


@bp.get("/")
async def index():
    return await render_template("index.html")


async def chat_coroutine():
    for i in range(5):
        yield {"choices": [{"delta": {"content": str(i/0)}}]}
        await asyncio.sleep(1)

@bp.post("/chat")
async def chat_handler():

    async def response_stream():
        async for event in chat_coroutine():
            yield json.dumps(event, ensure_ascii=False) + "\n"

    try:
        return Response(response_stream())
    except Exception as e:
        return jsonify({"choices": [{"delta": {"content": str(e)}}]})
