from japronto import Application

requests = 0

def hello(request):
	global requests
	requests += 1
	return request.Response(text=f'{requests}')

app = Application()

r = app.router
r.add_route('/', hello, method='GET')

app.run(port=9999, worker_num=200, debug=True)
