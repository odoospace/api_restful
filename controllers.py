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

    @http.route('/api/<model>', type='http', auth='public', cors='*')
    def search(self, model, token, offset=0, limit=None, fields='id', sort='id'):
        print model, token, fields
        token = http.request.env['apirest.token'].sudo().search([('token', '=', token)])
        res = {}
        if token:
            # magic
            """
            reg = registry(token.app_id.dbname)
            model = http.request.env[model]
            """
            model = http.request.env[model]
            data = model.sudo(token.user_id).search_read(
                fields = fields.split(','),
                offset = offset and int(offset) or 0,
                limit = limit and int(limit) or None
            )
            res = json.dumps(data)
        return res

    @http.route('/api/<model>/<field>/<op>/<value>', type='http', auth='public', cors='*')
    def search_by_field(self, model, field, op, value, token, offset=0, limit=None, fields='',):
        """ ex: /api/model/res.partner/name/=/john"""
        # TODO: use a json in searchs 
        token = http.request.env['apirest.token'].sudo().search([('token', '=', token)])
        res = {}
        if token:
            model = http.request.env[model]
            data = model.sudo(token.user_id).search_read(
                [(field, op, value)],
                fields=fields.split(','),
                offset = offset and int(offset) or 0,
                limit = limit and int(limit) or None
            )
            res = json.dumps(data[0])
        return res
