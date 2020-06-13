# -*- coding: utf-8 -*-

from odoo import models, fields, api
import uuid

class token(models.Model):
    _name = 'apirest.token'
    _description = 'Api rest token'


    def _get_uuid(self):
        return uuid.uuid4()

    # TODO: expire session
    # TODO: expire from create
    user_id = fields.Many2one('res.users', string='User')
    app_id = fields.Many2one('apirest.app', string='App', required=True)
    token = fields.Char(default=_get_uuid, readonly=True)
    created_at = fields.Datetime(default=fields.Datetime.now)
    active = fields.Boolean(default=True)


class app(models.Model):
    """Define apps to use apirest"""
    _name = 'apirest.app'
    _description = 'Api rest app'

    def _get_dbname(self):
        return self.env.cr.dbname

    name = fields.Char()
    description = fields.Char()
    sandbox = fields.Boolean()
    active = fields.Boolean(default=True)
    dbname = fields.Char(default=_get_dbname)
    created_at = fields.Datetime(default=fields.Datetime.now)
    token_ids = fields.One2many('apirest.token', 'app_id')
    # white lists (comma separated)
    whitelist_domains = fields.Char(string='Domains whitelist')
    whitelist_ips = fields.Char(string='IPs whitelist')
    # sql
    sql_ids = fields.One2many('apirest.sql', 'app_id')


class sql(models.Model):
    """define raw sql queries"""
    _name = 'apirest.sql'
    _description = 'SQL queries'

    name = fields.Char()
    description = fields.Char()
    active = fields.Boolean(default=True)
    query = fields.Char()
    app_id = fields.Many2one('apirest.app')


class res_users(models.Model):
    """extends res.users"""
    _inherit = 'res.users'

    token_ids = fields.One2many('apirest.token', 'user_id')
