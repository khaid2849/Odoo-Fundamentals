from odoo import models, fields, api


class VanPhongGiaoDich(models.Model):
    _name = "apartment.van.phong.giao.dich"
    _description = "Model Văn Phòng Giao Dịch"

    # Dia ch
    address = fields.Char(string="Địa chỉ", inverse="_inverse_address")
    country = fields.Many2one(
        string="Quốc gia", comodel_name="res.country", required=True
    )
    state = fields.Many2one(
        comodel_name="res.country.state",
        string="Tỉnh(Thành phố)",
        domain="[('country_id', '=', country)]",
        required=True,
    )
    district = fields.Many2one(
        comodel_name="apartment.district",
        string="Quận(Huyện)",
        domain="[('state_id', '=', state)]",
        required=True,
    )
    ward = fields.Many2one(
        comodel_name="apartment.district.ward",
        string="Phường(Xã)",
        domain="[('district_id', '=', quan)]",
        required=True,
    )
    street = fields.Char(string="Đường", required=True)

    customer_id = fields.One2many(
        string="Khách hàng",
        comodel_name="apartment.khach.hang",
        inverse_name="sales_office_id",
    )

    @api.depends("country", "state", "district", "ward", "street")
    def _inverse_address(self):
        for record in self:
            record.address = f"{record.street}, {record.ward}, {record.district}, {record.state}, {record.country}"
