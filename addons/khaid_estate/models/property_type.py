from odoo import models, fields


class PopertyType(models.Model):
    _name = "khaid.property_type"

    name = fields.Char(required=True, string="Property Type")
    description = fields.Text(string="Description")
