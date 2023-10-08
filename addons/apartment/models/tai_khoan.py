from odoo import models, fields


class TaiKhoan(models.Model):
    _name = "apartment.tai.khoan"
    _description = "Model Tài Khoản"

    name = fields.Char(string="Tên", required=True)
    email = fields.Char(string="Email đăng nhập", required=True)
    account_type = fields.Char(
        string="Loại tài khoản",
        required=True,
    )
    status = fields.Selection(
        string="Trạng thái",
        selection=[
            ("hoat_dong", "Hoạt động"),
            ("dung_hoat_dong", "Dừng hoạt động"),
        ],
        required=True,
    )
