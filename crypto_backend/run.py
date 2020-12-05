from aiohttp import web

routes = web.RouteTableDef()

@routes.get('/')
async def hello(request):
    return web.Response(text="Hello HPPL course")

app = web.Application()
app.add_routes(routes)
web.run_app(app)
