from odoo import models, fields


class PropertyType(models.Model):
    _name = "real.estate.property.type"
    _description = "Property Type model"
    _order = "name"

    name = fields.Char(required=True, string="Property Type")
    description = fields.Text(string="Description")
    property_ids = fields.One2many(
        comodel_name="real.estate.property",
        inverse_name="property_type_id",
        string="Property",
    )
    sequence = fields.Integer("Sequence")

    _sql_constraints = [
        ("uniq_name", "unique(name)", "A type name must be unique."),
    ]
