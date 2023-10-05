from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api


class PropertyOffer(models.Model):
    _name = "real.estate.property.offer"
    _description = "Property Offer model"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        string="Status",
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one(comodel_name="real.estate.property", required=True)
    validity = fields.Integer(inverse="_inverse_validity", default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_validity", store=True
    )

    _sql_constraints = [
        (
            "check_price",
            "CHECK(price > 0)",
            "An offer price must be strictly positive.",
        ),
    ]

    @api.depends("validity")
    # compute method is called at each change of its dependencies
    def _compute_date_deadline(self):
        for offer in self:
            validity = offer.validity
            create_date = offer.create_date or date.today()
            offer.date_deadline = create_date + relativedelta(days=validity)

    # inverse method is called when saving the record
    def _inverse_validity(self):
        for offer in self:
            offer.validity = (offer.date_deadline - (offer.create_date).date()).days

    def action_accept_offer(self):
        for offer in self:
            offer.status = "accepted"
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer = offer.partner_id
        return True

    def action_refuse_offer(self):
        for offer in self:
            offer.status = "refused"
        return True
