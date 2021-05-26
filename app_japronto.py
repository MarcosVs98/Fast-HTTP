from japronto import Application


def hello(request):
    return request.Response(text='H')


app = Application()

r = app.router
r.add_route('/', hello, method='GET')

app.run(port=9000, worker_num=200)
