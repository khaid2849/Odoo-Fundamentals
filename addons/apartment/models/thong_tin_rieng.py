from odoo import models, fields


class ThongTinRieng(models.Model):
    _name = "apartment.thong.tin.rieng"
    _description = "Model Thông tin riêng"

    name = fields.Char(string="Tên")
    gia_tri = fields.Char(string="Giá trị")
    ten_loai = fields.Char(string="Tên loại")
    nguoi_cap_nhat = fields.Char(string="Người cập nhật")
    hieu_luc = fields.Boolean(string="Hiệu lực")
    khach_hang_ids = fields.Many2one(
        string="Khách hàng", comodel_name="apartment.khach.hang"
    )
