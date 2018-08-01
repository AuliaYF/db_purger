# -*- coding: utf-8 -*-

from odoo import api, fields, models

PROTECTED_MODELS = [
    'db.purger',
    'db.purger.line'
]

DEFAULT_DOMAIN = [
    ('id', '!=', '-123456'),
]


class Purger(models.Model):
    _name = 'db.purger'
    _rec_name = 'name'
    _description = 'Purger'

    name = fields.Char(string="Name", required=False,
                       default=lambda self: "Purge {datetime}".format(datetime=fields.datetime.now()), readonly=True, )
    line_ids = fields.One2many(comodel_name="db.purger.line", inverse_name="purge_id", string="List of Model(s)",
                               required=False, )

    @api.onchange("name")
    def _default_line_ids(self):
        line_ids = []

        for model in self.env["ir.model"].search([("model", "=", "db.purger.demo")]):
            line_ids.append((0, 0, {
                "model_id": model.id
            }))

        self.line_ids = line_ids

    @api.multi
    def action_purge(self):
        for r in self:
            for line in r.line_ids:
                obj = self.pool.get(line.model_id.model)
                if obj and obj._table_exist:
                    sql = "delete from %s" % obj._table
                    self._cr.execute(sql)


class PurgerLine(models.Model):
    _name = 'db.purger.line'
    _rec_name = 'model_id'
    _description = 'Purger model lines'

    purge_id = fields.Many2one(comodel_name="db.purger", string="Purge ID", required=False, )
    model_id = fields.Many2one(comodel_name="ir.model", string="Model", required=True, ondelete='cascade', )

    @api.onchange("model_id")
    def _build_model_id_domain(self):
        model_ids = []

        models = self.env['ir.model'].search([])
        for model in models:
            if self.env.get(model.model) is None:
                model_ids.append(model.model)

        for model in PROTECTED_MODELS:
            model_ids.append(model)

        return {
            'domain': {
                'model_id': [('model', 'not in', model_ids)]
            }
        }
