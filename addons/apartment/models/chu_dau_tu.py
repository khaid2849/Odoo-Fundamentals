from odoo import models, fields


class ChuDauTu(models.Model):
    _name = "apartment.chu.dau.tu"
    _description = "Model Chủ đầu tư"

    ma = fields.Char(string="Mã", required=True)
    loai_dinh_danh = fields.Selection(
        string="Loại định danh",
        selection=[("ma_so_thue", "Mã số thuế"), ("khac", "Khác"), ])
    ma_dinh_danh = fields.Char(string="Mã định danh")
    ten = fields.Char(string="Tên")
    so_dien_thoai = fields.Char(string="Số điện thoại")
    email = fields.Char(string="Email")

    # Dia chi
    dia_chi = fields.Char(string="Địa chỉ")
    quoc_gia = fields.Many2one(string="Quốc gia", comodel_name="res.country", default="Việt Nam")
    tinh = fields.Many2one(comodel_name='res.country.state', string="Tỉnh(Thành phố)")
    # tinh = fields.Char(string="Tỉnh(Thành phố)")
    quan = fields.Char(string="Quận(Huyện)")
    phuong = fields.Char(string="Phường(Xã)")
    duong = fields.Char(string="Đường")

    nguoi_dai_dien = fields.Char(string="Người đại diện")
    chuc_vu = fields.Char(string="Chức vụ")
    ghi_chu = fields.Text(string="Ghi chú")

    _sql_constraints = [
        ("uniq_name", "unique(ma)", "Mã phải là duy nhất "),
        ("uniq_name", "unique(ma_dinh_danh)", "Mã định danh phải là duy nhất"),
    ]
