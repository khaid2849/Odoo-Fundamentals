from odoo import models, fields


class District(models.Model):
    _name = "apartment.district"
    _description = "District model"

    name = fields.Char(string="name")
    state_id = fields.Many2one(string="code", comodel_name="res.country.state")
    ward = fields.One2many(
        string="code",
        comodel_name="apartment.district.ward",
        inverse_name="district_id",
    )


class Ward(models.Model):
    _name = "apartment.district.ward"
    _description = "Ward model"

    name = fields.Char(string="name")
    district_id = fields.Many2one(string="code", comodel_name="apartment.district")
