from japronto import Application


def hello(request):
    return request.Response(text='H')


app = Application()

r = app.router
r.add_route('/', hello, method='GET')
r.add_route('/', hello, method='HEAD')

app.run(port=9999, worker_num=200)
