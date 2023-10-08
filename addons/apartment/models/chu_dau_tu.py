from odoo import models, fields, api


class ChuDauTu(models.Model):
    _name = "apartment.chu.dau.tu"
    _description = "Model Chủ đầu tư"

    code = fields.Char(string="Mã")
    identifier_type = fields.Selection(
        string="Loại định danh",
        selection=[
            ("ma_so_thue", "Mã số thuế"),
            ("khac", "Khác"),
        ],
        required=True,
    )
    identifier = fields.Char(string="Mã định danh", required=True)
    name = fields.Char(string="Tên", required=True)
    phone = fields.Char(string="Số điện thoại", required=True)
    email = fields.Char(string="Email", required=True)

    # Dia chi
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
        domain="[('district_id', '=', district)]",
        required=True,
    )
    street = fields.Char(string="Đường", required=True)

    representative = fields.Char(string="Người đại diện", required=True)
    position = fields.Char(string="Chức vụ")
    description = fields.Char(string="Ghi chú")

    @api.depends("country", "state", "district", "ward", "street")
    def _inverse_address(self):
        for record in self:
            record.address = f"{record.street}, {record.ward.name}, {record.district.name}, {record.state.name}, {record.country.name}"

    @api.model
    def create(self, vals):
        vals["code"] = self.env["ir.sequence"].next_by_code(
            "apartment.chu.dau.tu.sequence"
        ) or _("New")

        res = super(ChuDauTu, self).create(vals)
        return res

    _sql_constraints = [
        ("uniq_name", "unique(ma)", "Mã phải là duy nhất "),
        ("uniq_name", "unique(identifier)", "Mã định danh phải là duy nhất"),
    ]
