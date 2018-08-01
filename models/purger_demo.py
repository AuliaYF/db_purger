# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PurgerDemoModel(models.Model):
    _name = 'db.purger.demo'
    _rec_name = 'name'
    _description = 'Purger demo model'

    name = fields.Char(string="Name", required=False, )
