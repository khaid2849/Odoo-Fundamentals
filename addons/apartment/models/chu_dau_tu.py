from odoo import models, fields


class ChuDauTu(models.Model):
    _name = "appartment.chu.dau.tu"
    _description = "Model Chủ đầu tư"

    ma = fields.Char(string="Mã", required=True)
    loai_dinh_danh = fields.Char(string="Loại định danh")
    ma_dinh_danh = fields.Char()
    ten = fields.Char(string="Tên")
    so_dien_thoai = fields.Char(string="Số điện thoại")
    email = fields.Char(string="Email")
    quoc_gia = fields.Char(string="Quốc gia")
    tinh = fields.Char(string="Tỉnh(Thành phố)")
    quan = fields.Char(string="Quận(Huyện)")
    phuong = fields.Char(string="Phường(Xã)")
    duong = fields.Char(string="Đường")
    chuc_vu = fields.Char(string="Chức vụ")
    ghi_chu = fields.Text(string="Ghi chú")
    # nguoi_dai_dien_id = fields.Many2one(
    #     comodel_name="apartment.nguoi.dai.dien",
    #     string="Người đại diện",
    # )

    _sql_constraints = [
        ("uniq_name", "unique(ma)", "Mã phải là duy nhất "),
        ("uniq_name", "unique(ma_dinh_danh)", "Mã định danh phải là duy nhất"),
    ]
