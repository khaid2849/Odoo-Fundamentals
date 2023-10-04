from odoo import models, fields


class PropertyOffer(models.Model):
    _name = "real.estate.property.offer"

    price = fields.Float()
    status = fields.Selection(
        string="Status",
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one(comodel_name="real.estate.property", required=True)
