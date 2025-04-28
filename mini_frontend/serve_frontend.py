import asyncio
from aiohttp import web
import os

STATIC_DIR = './mini_frontend'  # Путь до папки с твоими HTML и JS

async def handle(request):
    return web.FileResponse(os.path.join(STATIC_DIR, 'index.html'))

async def create_app():
    app = web.Application()
    app.router.add_static('/', STATIC_DIR, show_index=True)
    app.router.add_route('GET', '/{tail:.*}', handle)  # Для всех остальных роутов - index.html
    return app

if __name__ == '__main__':
    app = asyncio.run(create_app())
    web.run_app(app, host='127.0.0.1', port=5173)
