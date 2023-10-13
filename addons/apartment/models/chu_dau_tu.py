import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError

phone_pattern = r"^\+\d{1,12}$"
email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
tax_pattern = r"^[0-9-]$"


class ChuDauTu(models.Model):
    _name = "apartment.chu.dau.tu"
    _description = "Model Chủ đầu tư"

    code = fields.Char(string="Mã")
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
    name = fields.Char(string="Tên", required=True)
    phone = fields.Char(string="Số điện thoại", required=True)
    email = fields.Char(string="Email", required=True)

    # Dia chi
    address = fields.Char(string="Địa chỉ", inverse="_inverse_address", reqired=True)
    country = fields.Many2one(
        string="Quốc gia",
        comodel_name="res.country",
        required=True,
        default=lambda self: self.env["res.country"].search([("code", "=", "VN")]),
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
    description = fields.Text(string="Ghi chú")
    active = fields.Boolean(default=False)
    partner_id = fields.Many2one(comodel_name="res.partner")

    @api.onchange("identifier", "phone", "email")
    def _onchange_remove_space(self):
        fields_to_process = ["identifier", "phone", "email"]
        for field in fields_to_process:
            field_value = getattr(self, field, False)
            if field_value and isinstance(field_value, str):
                setattr(self, field, field_value.replace(" ", ""))

    @api.depends("country", "state", "district", "ward", "street")
    def _inverse_address(self):
        for record in self:
            record.address = f"{record.street}, {record.ward.name}, {record.district.name}, {record.state.name}, {record.country.name}"

    @api.model
    def create(self, vals):
        vals["code"] = (
                self.env["ir.sequence"].next_by_code("apartment.chu.dau.tu.sequence")
                or "New"
        )

        partner_vals = {
            "name": vals.get("name"),
            "phone": vals.get("phone"),
            "email": vals.get("email"),
            "street": vals.get("street"),
            "state_id": vals.get("state", False),
            "country_id": vals.get("country", False),
            "vat": vals.get("identifier") if vals.get("identifier_type") == "ma_so_thue" else None
        }
        partner = self.env["res.partner"].create(partner_vals)
        vals["partner_id"] = partner.id
        return super(ChuDauTu, self).create(vals)

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

    _sql_constraints = [
        ("uniq_name", "unique(ma)", "Mã phải là duy nhất "),
        ("uniq_name", "unique(identifier)", "Mã định danh phải là duy nhất"),
    ]
