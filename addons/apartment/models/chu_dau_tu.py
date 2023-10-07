from odoo import models, fields, api


class ChuDauTu(models.Model):
    _name = "apartment.chu.dau.tu"
    _description = "Model Chủ đầu tư"

    ma = fields.Char(string="Mã")
    loai_dinh_danh = fields.Selection(
        string="Loại định danh",
        selection=[
            ("ma_so_thue", "Mã số thuế"),
            ("khac", "Khác"),
        ],
        required=True,
    )
    ma_dinh_danh = fields.Char(string="Mã định danh", required=True)
    name = fields.Char(string="Tên", required=True)
    so_dien_thoai = fields.Char(string="Số điện thoại", required=True)
    email = fields.Char(string="Email", required=True)

    # Dia chi
    dia_chi = fields.Char(string="Địa chỉ", inverse="_inverse_dia_chi")
    quoc_gia = fields.Many2one(
        string="Quốc gia", comodel_name="res.country", default="Việt Nam", required=True
    )
    tinh = fields.Many2one(
        comodel_name="res.country.state",
        string="Tỉnh(Thành phố)",
        domain="[('country_id', '=', quoc_gia)]",
        required=True,
    )
    quan = fields.Many2one(
        comodel_name="apartment.district",
        string="Quận(Huyện)",
        domain="[('state_id', '=', tinh)]",
        required=True,
    )
    phuong = fields.Many2one(
        comodel_name="apartment.district.ward",
        string="Phường(Xã)",
        domain="[('district_id', '=', quan)]",
        required=True,
    )
    duong = fields.Char(string="Đường", required=True)

    nguoi_dai_dien = fields.Char(string="Người đại diện", required=True)
    chuc_vu = fields.Char(string="Chức vụ")
    ghi_chu = fields.Char(string="Ghi chú")

    @api.depends("quoc_gia", "tinh", "quan", "phuong", "duong")
    def _inverse_dia_chi(self):
        for record in self:
            record.dia_chi = f"{record.duong}, {record.phuong.name}, {record.quan.name}, {record.tinh.name}, {record.quoc_gia.name}"

    _sql_constraints = [
        ("uniq_name", "unique(ma)", "Mã phải là duy nhất "),
        ("uniq_name", "unique(ma_dinh_danh)", "Mã định danh phải là duy nhất"),
    ]
