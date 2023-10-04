from odoo import models, fields


class PropertyType(models.Model):
    _name = "real.estate.property.type"

    name = fields.Char(required=True, string="Property Type")
    description = fields.Text(string="Description")
