from odoo import models, fields, api


class KhachHang(models.Model):
    _name = "apartment.khach.hang"
    _description = "Model Khách hàng"

    customer_type = fields.Selection(
        string="Loại khách hàng",
        required=True,
        selection=[
            ("to_chuc", "Tổ chức"),
            ("ca_nhan", "Cá nhân"),
        ],
    )
    identifier_type = fields.Char(string="Loại định danh", required=True)
    identifier = fields.Char(string="Mã định danh", required=True)
    customer_code = fields.Char(string="Mã khách hàng", required=True)
    name = fields.Char(string="Tên khách hàng", required=True)
    abbreviations = fields.Char(string="Tên viết tắt")
    email = fields.Char(string="Email", required=True)
    phone = fields.Char(string="Số điện thoại", required=True)
    employee_size = fields.Char(string="Quy mô nhân sự")
    business_areas = fields.Char(string="Lĩnh vực kinh doanh")

    # Dia chi
    address = fields.Char(
        string="Địa chỉ",
        inverse="_inverse_address",
        required=True,
    )
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

    rented_land_area = fields.Float(string="Diện tích đất thuê")
    representative = fields.Char(
        string="Người đại diện",
        required=True,
    )
    representative_phone = fields.Char(string="Số điện thoại người đại diện")
    representative_email = fields.Char(string="Email người đại diện")
    position = fields.Char(string="Chức vụ")
    description = fields.Char(string="Ghi chú")

    sales_office_id = fields.Many2one(
        comodel_name="apartment.van.phong.giao.dich",
        string="Văn phòng giao dịch",
    )
    private_information_ids = fields.One2many(
        comodel_name="apartment.thong.tin.rieng",
        inverse_name="customer_ids",
        string="Thông tin riêng",
    )

    @api.depends("country", "state", "district", "ward", "street")
    def _inverse_address(self):
        for record in self:
            record.address = f"{record.street}, {record.ward}, {record.district}, {record.state}, {record.country}"

    @api.model
    def create(self, vals):
        vals["customer_code"] = self.env["ir.sequence"].next_by_code(
            "apartment.khach.hang.sequence"
        ) or _("New")

        res = super(KhachHang, self).create(vals)
        return res

    _sql_constraints = [
        ("uniq_name", "unique(identifier)", "Mã định danh phải là duy nhất "),
        ("uniq_name", "unique(customer_code)", "Mã khách hàng phải là duy nhất "),
    ]
