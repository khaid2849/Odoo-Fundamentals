import re
from odoo import models, fields, api
from odoo.exceptions import ValidationError

phone_pattern = r"^\+\d{1,12}$"
email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
tax_pattern = r"^[\d-]+"


class NhaCungCap(models.Model):
    _name = "apartment.nha.cung.cap"
    _description = "Model Nhà cung cấp"

    code = fields.Char(string="Mã nhà cung cấp")
    name = fields.Char(required=True, string="Tên nhà cung cấp")
    identifier = fields.Char(required=True, string="Mã định danh")
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
    phone = fields.Char(required=True, string="Số điện thoại")
    email = fields.Char(required=True, string="Email")

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
    person_in_charge = fields.Char(string="Người phụ trách", required=True)
    position = fields.Char(string="Chức vụ")
    description = fields.Text(string="Ghi chú")
    start_date = fields.Date(string="Ngày bắt đầu hợp tác", required=True)
    end_date = fields.Date(string="Ngày kết thúc hợp tác")
    contract = fields.Binary(string="Hợp đồng hợp tác", required=True)
    dich_vu_ids = fields.One2many(string="Dịch vụ", comodel_name="apartment.dich.vu", inverse_name="provider")
    partner_id = fields.Many2one(comodel_name="res.partner")
    active = fields.Boolean(default=True)

    def find_existing_chu_dau_tu_khach_hang(self, model: str, identifier, identifier_type):
        chu_dau_tu = self.env[model].search([
            ("active", "=", True),
            ("identifier", "=", identifier),
            ("identifier_type", "=", identifier_type),
        ])
        return chu_dau_tu

    @api.model
    def create(self, vals):
        vals["code"] = (
                self.env["ir.sequence"].next_by_code("apartment.nha.cung.cap.sequence")
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
        existing_chu_dau_tu = self.find_existing_chu_dau_tu_khach_hang("apartment.chu.dau.tu", vals.get("identifier"),
                                                                       vals.get("identifier_type"))
        existing_khach_hang = self.find_existing_chu_dau_tu_khach_hang("apartment.khach.hang", vals.get("identifier"),
                                                                       vals.get("identifier_type"))

        if existing_chu_dau_tu or existing_khach_hang:
            partner = self.env["res.partner"].search([("id", "=", existing_chu_dau_tu.partner_id.id)])
            partner.update(partner_vals)
        else:
            partner_vals["is_company"] = True
            self.env["res.partner"].create(partner_vals)

        vals["partner_id"] = self.env["res.partner"].id
        return super(NhaCungCap, self).create(vals)

    @api.depends("country", "state", "district", "ward", "street")
    def _inverse_address(self):
        for record in self:
            record.address = f"{record.street}, {record.ward.name}, {record.district.name}, {record.state.name}, {record.country.name}"

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

    @api.onchange("identifier", "phone", "email")
    def _onchange_remove_space(self):
        fields_to_process = ["identifier", "phone", "email"]
        for field in fields_to_process:
            field_value = getattr(self, field, False)
            if field_value and isinstance(field_value, str):
                setattr(self, field, field_value.replace(" ", ""))

    @api.onchange("name")
    def _onchange_name(self):
        if self.name:
            self.name.capitalize()

    @api.onchange("end_date")
    def _check_end_date(self):
        if self.end_date and self.end_date <= self.start_date:
            self.end_date = None
            return {"warning": {
                "title": "Warning",
                "message": "Ngày kết thúc hợp tác phải sau Ngày bắt đầu hợp tác!"
            }}

    def get_dich_vu(self):
        self.ensure_one()
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Danh mục dịch vụ',
            'view_mode': 'tree',
            'res_model': 'apartment.dich.vu',
            'domain': [('provider', '=', self.id)],
            'context': "{'create': False}"
        }

    _sql_constraints = [
        ("uniq_name", "unique(identifier)", "Mã định danh phải là duy nhất"),
    ]
