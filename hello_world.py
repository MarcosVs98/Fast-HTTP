from japronto import Application
import asyncio

def hello(request):
    return request.Response(text='Hello world!')

def hello(request):
    return request.Response(json={'hello': 'world'})

async def hello(request):
    return request.Response(text='Hello world!')

if __name__ == '__main__':

	app = Application()
	app.router.add_route('/', hello)
	app.run(debug=True,worker_num=200)