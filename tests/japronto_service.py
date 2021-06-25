from japronto import Application

def hello(request):
	return request.Response(text='hello wolrd')

app = Application()
r = app.router
r.add_route('/', hello, method='GET')

app.run(port=9999, worker_num=200, debug=True)

# end-of-file