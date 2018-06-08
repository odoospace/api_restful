# -*- coding: utf-8 -*-

from openerp import models, fields, api
import uuid

class token(models.Model):
     _name = 'api_restful.token'

     def get_uuid(self):
         return uuid.uuid4()

     db = fields.Char()
     uid = fields.Char()
     token = fields.Char(default=get_uuid)
     created_at = fields.Datetime(default=fields.Datetime.now)
