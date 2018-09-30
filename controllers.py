# -*- coding: utf-8 -*-
from openerp import http, registry
import json

class ApiRestful(http.Controller):
    """
    @http.route('/api/auth/get_token', type='http', auth='public', cors='*')
    def get_token(self, db='', user='', password=''):
        wsgienv = http.request.httprequest.environ
        env = dict(
            base_location=http.request.httprequest.url_root.rstrip('/'),
            HTTP_HOST=wsgienv['HTTP_HOST'],
            REMOTE_ADDR=wsgienv['REMOTE_ADDR'],
        )
        uid = http.dispatch_rpc('common', 'authenticate', [db, user, password, env])
        data = {
            'db': db,
            'uid': uid
        }
        token = http.request.env['api_restful.token'].sudo().create(data)
        return json.dumps({ 'token': token.token })
    """

    @http.route('/api/search/<model>', type='json', auth='public', methods=['POST'], cors='*', csrf=False)
    def search(self, model, **kwargs):
        """
        {
            'token': xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx', 
            'condition': [{ 'id', '=', 25}, {'date', '>=', '2017/05/21'}],
            'fields': ['id', 'name']
        }
        """

        token = kwargs['token']
        condition = kwargs.get('condition', [])
        fields = kwargs['fields']
        offset = kwargs.get('offset', 0)
        limit = kwargs.get('limit', None)
        sort = kwargs.get('sort', 'id')
        context = kwargs.get('context', {})

        t = http.request.env['apirest.token'].sudo().search([('token', '=', token)])
        payload = {}
        if t: 
            # magic
            """
            reg = registry(t.app_id.dbname)
            model = http.request.env[model]
            """
            model = http.request.env[model]
            res = model.sudo(t.user_id).with_context(**context).search_read(
                condition,
                fields = fields,
                offset = offset and int(offset) or 0,
                limit = limit and int(limit) or None
            )
            payload = json.dumps(res)
        return payload


    @http.route('/api/update/<model>/<id>', type='json', auth='public', methods=['POST'], cors='*', csrf=False)
    def update(self, model, id, **kwargs):
        """
        {
            'token': xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx', 
            'data': {'name': 'newname'}
        }
        """

        token = kwargs['token']
        data = kwargs['data']

        print token, data

        t = http.request.env['apirest.token'].sudo().search([('token', '=', token)])
        payload = {}
        if t: 
            # magic
            """
            reg = registry(t.app_id.dbname)
            model = http.request.env[model]
            """
            model = http.request.env[model]
            res = model.sudo(t.user_id).search([('id', '=', id)]).write(data)
            payload = json.dumps(res)
        return payload

    @http.route('/api/create/<model>', type='json', auth='public', methods=['POST'], cors='*', csrf=False)
    def create(self, model, **kwargs):
        """
        {
            'token': xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx', 
            'data': {'name': 'newname'}
        }
        """

        token = kwargs['token']
        data = kwargs['data']

        t = http.request.env['apirest.token'].sudo().search([('token', '=', token)])
        payload = {}
        if t: 
            # magic
            """
            reg = registry(t.app_id.dbname)
            model = http.request.env[model]
            """
            model = http.request.env[model]
            res = model.sudo(t.user_id).create(data)
            if res:
                payload = json.dumps(res.id)
        return payload

    @http.route('/api/execute/<model>/<id>/<function>', type='json', auth='public', methods=['POST'], cors='*', csrf=False)
    def execute(self, model, id, function, **kwargs):
        """
        {
            'token': xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx', 
            'data': {'name': 'newname'}
        }
        """

        token = kwargs['token']

        t = http.request.env['apirest.token'].sudo().search([('token', '=', token)])
        payload = {}
        if t: 
            # magic
            """
            reg = registry(t.app_id.dbname)
            model = http.request.env[model]
            """
            model = http.request.env[model]
            res = getattr(model.sudo(t.user_id).search([('id', '=', id)])[0], function)() 
            if res:
                payload = json.dumps(res)
        return payload

    @http.route('/api/delete/<model>/<id>', type='json', auth='public', methods=['POST'], cors='*', csrf=False)
    def delete(self, model, id, **kwargs):
        """
        {
            'token': xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx', 
            'data': {'name': 'newname'}
        }
        """

        token = kwargs['token']

        t = http.request.env['apirest.token'].sudo().search([('token', '=', token)])
        payload = {}
        if t: 
            # magic
            """
            reg = registry(t.app_id.dbname)
            model = http.request.env[model]
            """
            model = http.request.env[model]
            res = model.sudo(t.user_id).search([('id', '=', id)]).unlink()
            if res:
                payload = json.dumps(res)
        return payload