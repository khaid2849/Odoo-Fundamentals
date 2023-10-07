from odoo import models, fields


class SoDoKCN(models.Model):
    _name = "apartment.so.do.kcn"
    _description = "Model Sơ đồ khu công nghiệp "

    name = fields.Char(string="Tên sơ đồ", required=True)
    dien_tich = fields.Float(string="Diện tích", required=True)
    dia_chi = fields.Char(string="Địa chỉ")
    tep_tin_so_do = fields.Binary(string="Tệp tin sơ đồ", required=True)
    url = fields.Char(string="Url")
