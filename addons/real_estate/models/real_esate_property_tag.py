from odoo import models, fields


class PropertyTag(models.Model):
    _name = "real.estate.property.tag"
    _description = "Property Tag model"
    _order = "name"

    name = fields.Char(required=True)
    description = fields.Text(string="Description")
    color = fields.Integer()

    _sql_constraints = [
        ("uniq_name", "unique(name)", "A tag name must be unique."),
    ]
