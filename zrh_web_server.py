from microdot_asyncio import Microdot
app = Microdot()

htmldoc = '''<!DOCTYPE html>
<html>
    <head>
        <title>Microdot Example Page</title>
        <meta charset="UTF-8">
    </head>
    <body>
        <div>
            <h1>Microdot Example Page</h1>
            <p>Hello from Microdot!</p>
            <p><a href="/shutdown">Click to shutdown the server</a></p>
        </div>
    </body>
</html>
'''


@app.route('/')
async def hello(request):
    return htmldoc, 200, {'Content-Type': 'text/html'}


@app.route('/shutdown')
async def shutdown(request):
    request.app.shutdown()
    return 'The server is shutting down...'

@app.errorhandler(404)
def not_found(request):
    return {'error': 'resource not found'}, 404


async def do_web_server():
    app.run(debug=True,port=8080)