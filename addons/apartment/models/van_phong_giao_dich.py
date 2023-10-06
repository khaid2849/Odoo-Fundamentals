from odoo import models, fields


class VanPhongDaiDien(models.Model):
    _name = "apartment.van.phong.giao.dich"
    _description = "Model Văn Phòng Giao Dịch"

    quoc_gia = fields.Char(string="Quốc gia")
    tinh = fields.Char(string="Tỉnh(Thành phố)")
    quan = fields.Char(string="Quận(Huyện)")
    phuong = fields.Char(string="Phường(Xã)")
    duong = fields.Char(string="Đường")
    khach_hang_id = fields.One2many(
        string="Khách hàng",
        comodel_name="apartment.khach.hang",
        inverse_name="van_phong_giao_dich_id",
    )
