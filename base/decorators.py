import json
from functools import wraps
from inspect import signature
import inspect
from base import http_exceptions as http


def convert_to_type_or_raise_exception(name, p, t):
    try:
        if t == int:
            return int(p)

        if t == float:
            return float(p)

    except Exception as e:
        tt = str(t).split("'")[1]
        raise http.HttpInvalidParam(id_message='INVALID_PARAM',
                                    message=f"Invalid type for param {p}, {tt} is expected")

    return p


def pack_error(origin_self, e):
    try:
        origin_self.set_status(e.status())
        err = e._dict()
    except:
        origin_self.set_status(http.status.INTERNAL_SERVER_ERROR)
        err = {'error': True}

    origin_self.write(json.dumps(err))


class api:

    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, funct):

        @wraps(funct)
        async def wrapper(_origin_self, *args, **kwargs):
            sig = signature(funct)

            body = {}
            if _origin_self.request.body:
                body = json.loads(_origin_self.request.body.decode('utf-8'))

            params = {}

            try:

                for p in sig.parameters:
                    if p == 'self':
                        continue

                    v = _origin_self.get_arguments(sig.parameters[p].name)

                    if len(v) > 1:
                        raise http.HttpInvalidParam(id_message='INVALID_PARAM',
                                                    message="Multiple params for signle key is not supported")

                    if len(v) == 1:
                        params[p] = v[0]

                    sp = sig.parameters[p]

                    if p in body and p in params:
                        if sp.default is sig.empty:
                            raise http.HttpInvalidParam(id_message='INVALID_PARAM',
                                                        message=f"Same param '{p}' presented in body and in query argument")

                    elif p not in params and p not in body:
                        if sp.default is sig.empty:
                            raise http.HttpInvalidParam(id_message='MISSING_PARAM',
                                                        message=f"Mandatory argument {p} is not provided")
                        else:
                            params[p] = sp.default
                    elif p in params and p not in body:
                        pass
                    else:
                        params[p] = body[p]

                    if params[p]:
                        params[p] = convert_to_type_or_raise_exception(p, params[p], sp.annotation)

            except Exception as e:
                return pack_error(_origin_self, e)

            _args = []

            res = await funct(_origin_self, *_args, **params)

            _origin_self.set_status(http.status.OK if res else http.status.NO_CONTENT)
            _origin_self.write(json.dumps(res, indent=1))

        return wrapper


class route:
    uri = []
    _handlers = []
    _global_settings = {}
    _handler_names = set()

    @staticmethod
    def all():
        return route._handlers

    @staticmethod
    def print_all_routes():
        print("---[", 'routes', "]" + ('-' * 47))
        for r in route.all():
            print("ROUTE", r)

        print("-" * 60)

    @staticmethod
    def set(key, value):
        route._global_settings[key] = value

    @staticmethod
    def get(key, default=None):
        if key in route._global_settings:
            return route._global_settings[key]

        return default

    @staticmethod
    def register_handler(uri, handler):
        for _uri, _ in route._handlers:
            if _uri == uri:
                raise http.HttpInternalServerError(f"Error creating api, endopoint '{_uri}'  already exists")

        route._handlers.append((uri, handler))

    @staticmethod
    def handlers():
        return sorted(route._handlers, reverse=True)

    @staticmethod
    def handler_names():
        return route._handler_names

    @staticmethod
    def set_handler_names(hn):
        route._handler_names = hn

    def __init__(self, URI='/?', *args, **kwargs):

        self.uri = []

        uris = [URI] if type(URI) == str else URI

        specified_prefix = kwargs['PREFIX'] if 'PREFIX' in kwargs else None

        for uri in uris:
            parts = uri.split('/')
            rparts = []
            for p in parts:
                rparts.append("([^/]*)" if len(p) and p[0] == ':' else p)

            self.uri.append({'specified_prefix': specified_prefix, 'route': '/'.join(rparts)})

    def __call__(self, cls):

        scls = str(cls).replace("<class '", "").replace("'>", "")
        svc = scls.split('.')

        self.handler_name = svc[-1]

        route_handler_names = route.handler_names()

        if self.handler_name in route_handler_names:
            raise http.HttpInternalServerError(
                f"Handler with class {self.handler_name} already defined in project, use unique class name")

        route_handler_names.add(self.handler_name)
        route.set_handler_names(route_handler_names)

        prefix = route.get('prefix', '')

        for duri in self.uri:
            uri = duri['route']
            default_prefix = prefix + ('/' if len(uri) > 0 and uri[0] != '/' else '')
            if duri['specified_prefix'] is not None:
                default_prefix = duri['specified_prefix'].strip()

            furi = default_prefix + uri

            furi = furi.strip()
            if furi[-1] == '/':
                furi += '?'
            elif furi[-1] != '?':
                furi += '/?'

            route.register_handler(furi, cls)
        return cls
