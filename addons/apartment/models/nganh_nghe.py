from odoo import models, fields


class NganhNghe(models.Model):
    _name = "apartment.nganh.nghe"
    _description = "Model Ngành nghề"

    ma = fields.Char(string="Mã")
    ten = fields.Char(string="Tên")
    ghi_chu = fields.Text(string="Ghi chú")
    nguoi_cap_nhat = fields.Char(string="Người cập nhật")

    _sql_constraints = [
        ("uniq_name", "unique(ma)", "Mã phải là duy nhất "),
    ]
