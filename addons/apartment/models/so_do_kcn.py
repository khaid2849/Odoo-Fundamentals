from odoo import models, fields


class SoDoKCN(models.Model):
    _name = "apartment.so.do.kcn"
    _description = "Model Sơ đồ khu công nghiệp "

    name = fields.Char(string="Tên sơ đồ", required=True)
    acreage = fields.Float(string="Diện tích", required=True)
    address = fields.Char(string="Địa chỉ")
    diagram_file = fields.Image(string="Tệp tin sơ đồ", required=True)
    url = fields.Char(string="Url")
    active = fields.Boolean()
