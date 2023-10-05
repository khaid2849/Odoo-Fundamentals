from odoo import models, fields


class TaiKhoan(models.Model):
    _name = "apartment.tai.khoan"
    _description = "Model Tài Khoản"

    ten = fields.Char(string="Tên", required=True)
    email = fields.Char(string="Email đăng nhập")
    loai_tai_khoan = fields.Char(string="Loại tài khoản")
    trang_thai = fields.Selection(
        string="Trạng thái",
        selection=[
            ("hoat_dong", "Hoạt động"),
            ("dung_hoat_dong", "Dừng hoạt động"),
        ],
    )
