from odoo import models, fields, api


class NhaCungCap(models.Model):
    _name = "apartment.nha.cung.cap"
    _description = "Model Nhà cung cấp"

    code = fields.Char(required=True, string="Mã nhà cung cấp")
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
    active = fields.Boolean()

    @api.depends("country", "state", "district", "ward", "street")
    def _inverse_address(self):
        for record in self:
            record.address = f"{record.street}, {record.ward.name}, {record.district.name}, {record.state.name}, {record.country.name}"

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
