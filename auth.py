import base
import base.app


@base.route('/auth/users')
class AuthHandler(base.Base):

    @base.api()
    async def get(self):
        return {'method': 'get - auth'}

    @base.api()
    async def post(self):
        return {'method': 'post'}


@base.route('/auth/sessions')
class SessionHandler(base.Base):

    @base.api()
    async def get(self):
        return {'method': 'get'}

    @base.api()
    async def post(self):
        return {'method': 'post'}

