from odoo import models, fields, api


class VanPhongGiaoDich(models.Model):
    _name = "apartment.van.phong.giao.dich"
    _description = "Model Văn Phòng Giao Dịch"

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

    khach_hang_id = fields.One2many(
        string="Khách hàng",
        comodel_name="apartment.khach.hang",
        inverse_name="van_phong_giao_dich_id",
    )

    @api.depends("quoc_gia", "tinh", "quan", "phuong", "duong")
    def _inverse_dia_chi(self):
        for record in self:
            record.dia_chi = f"{record.duong}, {record.phuong}, {record.quan}, {record.tinh}, {record.quoc_gia}"
