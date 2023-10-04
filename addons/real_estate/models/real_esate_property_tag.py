from odoo import models, fields


class PropertyTag(models.Model):
    _name = "real.estate.property.tag"

    name = fields.Char(required=True)
    description = fields.Text(string="Description")
