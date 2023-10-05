from odoo import models, fields


class NguoiDaiDien(models.Model):
    _name = "apartment.nguoi.dai.dien"
    _description = "Model Người đại diện"

    ten = fields.Char(string="Tên người đại diện", required=True)
    email = fields.Char(string="Email người đại diện")
    chuc_vu = fields.Char(string="Chức vụ người đại diện")
    so_dien_thoai = fields.Char(string="Sđt người đại diện")
    ghi_chu = fields.Text(string="Ghi chú")
    # khach_hang_ids = fields.One2many(
    #     comodel_name="apartment.khach.hang",
    #     inverse_name="nguoi_dai_dien_id",
    #     string="Khách hàng",
    # )
    # chu_dau_tu_ids = fields.One2many(
    #     comodel_name="apartment.chu.dau.tu",
    #     inverse_name="nguoi_dai_dien_id",
    #     string="Chủ đầu tư",
    # )
