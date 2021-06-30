import tornado
from base.decorators import route


def make_app(print_routes=True, debug=True):
    r = []
    for i in route.handlers():
        r.append((r'{}'.format(i[0]), i[1]))

    if print_routes:
        route.print_all_routes()

    app = tornado.web.Application(r, debug=debug, autoreload=False)
    return app


def run(port=8888, print_routes=True, debug=True):
    app = make_app(print_routes, debug)
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()
