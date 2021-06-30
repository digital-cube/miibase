import base
import base.app

@base.route('/no-param-route')
class NoParamRouteHandler(base.Base):

    @base.api()
    async def get(self):
        return {'method': 'get'}

    @base.api()
    async def post(self):
        return {'method': 'post'}

    @base.api()
    async def patch(self):
        return {'method': 'patch'}

    @base.api()
    async def delete(self):
        return {'method': 'delete'}


@base.route('/int-param-route')
class IntParamHandler(base.Base):
    @base.api()
    async def get(self, i_param: int):
        return {'method': 'get', 'type': str(type(i_param)).split("'")[1], 'value': i_param}

    @base.api()
    async def post(self, i_param: int):
        return {'method': 'post', 'type': str(type(i_param)).split("'")[1], 'value': i_param}


@base.route('/optional-int-param-route')
class OptionalIntParamHandler(base.Base):
    @base.api()
    async def get(self, i_param: int = 42):
        return {'method': 'get', 'type': str(type(i_param)).split("'")[1], 'value': i_param}


@base.route('/float-param-route')
class FloatParamHandler(base.Base):
    @base.api()
    async def get(self, f_param: float):
        return {'method': 'get', 'type': str(type(f_param)).split("'")[1], 'value': f_param}

@base.route('/list-param-route')
class ListParamHandler(base.Base):
    @base.api()
    async def post(self, l_param: list):
        return {'method': 'get', 'type': str(type(l_param)).split("'")[1], 'value': l_param}



# @route('/')
# class IndexHandler():
#
#     @api()
#     async def get(self): #, iparam: int, fparam:float, sparam: str = 'test', lparam: list = [], dparam: dict={}):
#         return {'method': 'get'}
#

if __name__ == "__main__":
    base.app.run()
