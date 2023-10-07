from odoo import models, fields, api


class KhachHang(models.Model):
    _name = "apartment.khach.hang"
    _description = "Model Khách hàng"

    loai_khach_hang = fields.Selection(
        string="Loại khách hàng",
        required=True,
        selection=[
            ("to_chuc", "Tổ chức"),
            ("ca_nhan", "Cá nhân"),
        ],
    )
    loai_dinh_danh = fields.Char(string="Loại định danh", required=True)
    ma_dinh_danh = fields.Char(string="Mã định danh", required=True)
    ma_khach_hang = fields.Char(string="Mã khách hàng", required=True)
    name = fields.Char(string="Tên khách hàng", required=True)
    ten_viet_tat = fields.Char(string="Tên viết tắt")
    email = fields.Char(string="Email", required=True)
    so_dien_thoai = fields.Char(string="Số điện thoại", required=True)
    quy_mo_nhan_su = fields.Char(string="Quy mô nhân sự")
    linh_vuc_kinh_doanh = fields.Char(string="Lĩnh vực kinh doanh")

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

    dien_tich_dat_thue = fields.Float(string="Diện tích đất thuê")
    nguoi_dai_dien = fields.Char(string="Người đại diện")
    chuc_vu = fields.Char(string="Chức vụ")
    ghi_chu = fields.Char(string="Ghi chú")

    van_phong_giao_dich_id = fields.Many2one(
        comodel_name="apartment.van.phong.giao.dich",
        string="Văn phòng giao dịch",
    )
    thong_tin_rieng_ids = fields.One2many(
        comodel_name="apartment.thong.tin.rieng",
        inverse_name="khach_hang_ids",
        string="Thông tin riêng",
    )

    @api.depends("quoc_gia", "tinh", "quan", "phuong", "duong")
    def _inverse_dia_chi(self):
        for record in self:
            record.dia_chi = f"{record.duong}, {record.phuong}, {record.quan}, {record.tinh}, {record.quoc_gia}"

    _sql_constraints = [
        ("uniq_name", "unique(ma_dinh_danh)", "Mã định danh phải là duy nhất "),
        ("uniq_name", "unique(ma_khach_hang)", "Mã khách hàng phải là duy nhất "),
    ]
