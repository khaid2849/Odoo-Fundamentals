from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import date
from dateutil.relativedelta import relativedelta


class EstateProperty(models.Model):
    _name = "real.estate.property"
    _description = "Property model"
    _order = "id desc"
    # _inherit = "real.estate.property"

    name = fields.Char(string="Estate Property Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(
        string="Date Availability",
        default=date.today() + relativedelta(months=3),
        copy=False,
    )
    expected_price = fields.Float()
    selling_price = fields.Float(
        string="Selling Price",
        read_only=True,
        copy=False,
    )
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
    property_type_id = fields.Many2one(
        comodel_name="real.estate.property.type", string="Property Type"
    )
    buyer = fields.Many2one(
        comodel_name="res.partner",
        string="Buyer",
        compute="_compute_offer_status",
        store=True,
    )
    seller = fields.Many2one(
        comodel_name="res.users", string="Seller", default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many(comodel_name="real.estate.property.tag", string="Tags")
    offer_ids = fields.One2many(
        comodel_name="real.estate.property.offer",
        inverse_name="property_id",
        string="Offers",
    )
    total_area = fields.Float(compute="_compute_total_area")
    best_offer = fields.Float(compute="_compute_best_offer")

    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "A property expected price must be strictly positive.",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price >= 0)",
            "A property selling price must be strictly positive.",
        ),
    ]

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_offer(self):
        for property in self:
            property.best_offer = max(property.offer_ids.mapped("price"), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        self.garden_area, self.garden_orientation = 0, None
        if self.garden:
            self.garden_area, self.garden_orientation = 10, "north"

    @api.constrains("selling_price")
    def _check_selling_price(self):
        for property in self:
            validate_selling_price = property.expected_price * 0.9
        if (
            property.offer_ids.status == "accepted"
            and property.selling_price < validate_selling_price
        ):
            raise ValidationError(
                "The selling price cannot be lower than 90% of the expected price."
            )

    def action_cancel_porperty(self):
        for property in self:
            if property.state != "sold":
                property.state = "canceled"
            else:
                raise UserError("A sold property cannot be canceled")
        return True

    def action_sold_property(self):
        for property in self:
            if property.state != "canceled":
                property.state = "sold"
            else:
                raise UserError("A canceled property cannot be set as sold")
        return True
