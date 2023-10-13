import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError

phone_pattern = r"^\+\d{1,12}$"
email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
tax_pattern = r"^(?=.*[0-9])(?=.*-)[0-9-]+$"


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
    identifier_type = fields.Selection(
        string="Loại định danh",
        selection=[
            ("ma_so_thue", "Mã số thuế"),
            ("ma_ngan_sach", "Mã ngân sách"),
            ("so_quyet_dinh", "Số quyết định"),
            ("giay_phep_dau_tu", "Giấy phép đầu tư"),
            ("ma_so_bhxh", "Mã số BHXH"),
            ("can_cuoc_cong_dan", "Căn cước công dân"),
            ("chung_minh_nhan_dan", "Chứng minh nhân dân"),
            ("ho_chieu", "Hộ chiếu"),
            ("khac", "Khác"),
        ],
        required=True,
    )
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

    rented_land_area = fields.Char(string="Diện tích đất thuê")
    representative = fields.Char(
        string="Người đại diện",
        required=True,
    )
    representative_phone = fields.Char(string="Số điện thoại người đại diện")
    representative_email = fields.Char(string="Email người đại diện")
    position = fields.Char(string="Chức vụ")
    description = fields.Text(string="Ghi chú")

    # Dia chi van phong giao dich
    sales_office_address = fields.Char(string="Văn phòng giao dịch")
    so_country = fields.Many2one(
        string="Quốc gia", comodel_name="res.country", required=True
    )
    so_state = fields.Many2one(
        comodel_name="res.country.state",
        string="Tỉnh(Thành phố)",
        domain="[('country_id', '=', country)]",
        required=True,
    )
    so_district = fields.Many2one(
        comodel_name="apartment.district",
        string="Quận(Huyện)",
        domain="[('state_id', '=', state)]",
        required=True,
    )
    so_ward = fields.Many2one(
        comodel_name="apartment.district.ward",
        string="Phường(Xã)",
        domain="[('district_id', '=', district)]",
        required=True,
    )
    so_street = fields.Char(string="Đường", required=True)

    private_information_ids = fields.One2many(
        comodel_name="apartment.thong.tin.rieng",
        inverse_name="customer_ids",
        string="Thông tin riêng",
    )
    active = fields.Boolean(default=True)

    @api.onchange("name")
    def _onchange_name(self):
        if self.customer_type == "to_chuc":
            self.name.upper()
        if self.customer_type == "ca_nhan":
            self.name.capitalize()

    @api.depends(
        "country",
        "state",
        "district",
        "ward",
        "street",
        "so_country",
        "so_state",
        "so_district",
        "so_ward",
        "so_street",
    )
    def _inverse_address(self):
        for record in self:
            address_fields = [
                record.street,
                record.ward,
                record.district,
                record.state,
                record.country,
            ]
            so_address_fields = [
                record.so_street,
                record.so_ward,
                record.so_district,
                record.so_state,
                record.so_country,
            ]
            record.address = ", ".join(filter(None, address_fields))
            record.sales_office_address = ", ".join(filter(None, so_address_fields))

    @api.constrains("phone")
    def _check_phone_number(self):
        for record in self:
            if not re.match(phone_pattern, record.phone):
                raise ValidationError("Định dạng số điện thoại không hợp lệ!")

    @api.constrains("email")
    def _check_email(self):
        for record in self:
            if not re.match(email_pattern, record.email):
                raise ValidationError("Định dạng email không hợp lệ!")

    @api.constrains("identifier")
    def _check_tax_id(self):
        for record in self:
            if record.identifier_type == "ma_so_thue":
                tax_id = record.identifier.replace(" ", "")
                if len(tax_id) > 13:
                    raise ValidationError("Định dạng mã số thuế không hợp lệ!")
                if not re.match(tax_pattern, tax_id):
                    raise ValidationError("Định dạng mã số thuế không hợp lệ!")
                if "-" in tax_id[0] or "-" in tax_id[-1] or "--" in tax_id:
                    raise ValidationError("Định dạng mã số thuế không hợp lệ!")

    @api.model
    def create(self, vals):
        vals["customer_code"] = (
            self.env["ir.sequence"].next_by_code("apartment.khach.hang.sequence")
            or "New"
        )

        res = super(KhachHang, self).create(vals)
        return res

    _sql_constraints = [
        ("uniq_name", "unique(identifier)", "Mã định danh phải là duy nhất "),
        ("uniq_name", "unique(customer_code)", "Mã khách hàng phải là duy nhất "),
    ]
