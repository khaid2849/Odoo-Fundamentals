from odoo import models, fields


class SoDoKCN(models.Model):
    _name = "apartment.so.do.kcn"
    _description = "Model Sơ đồ khu công nghiệp "

    name = fields.Char(string="Tên sơ đồ", required=True)
    acreage = fields.Float(string="Diện tích", required=True)
    uom = fields.Many2one(string="Đơn vị tính", comodel_name="uom.uom", required=True)
    address = fields.Char(string="Địa chỉ", required=True)
    diagram_file = fields.Image(string="Tệp tin sơ đồ", required=True)
    description = fields.Char(string="Mô tả")
    active = fields.Boolean(default=True)
