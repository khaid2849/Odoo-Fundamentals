from odoo import models, fields
from datetime import date
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "khaid.estate_property"

    name = fields.Char(string="Estate Property Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        string="Date Availability",
        default=date.today() + relativedelta(months=3),
        copy=False,
    )
    expected_price = fields.Float()
    selling_price = fields.Float(string="Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    active = fields.Boolean(default=False)
    state = fields.Selection(
        string="State",
        required=True,
        selection=[
            ("new", "New"),
            ("offer_recevied", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        default="new",
    )
    property_type_id = fields.Many2one("khaid.property_type", string="Property Type")
    buyer = fields.Many2one("res.partner", string="Buyer")
    seller = fields.Many2one(
        "res.users", string="Seller", default=lambda self: self.env.user
    )
