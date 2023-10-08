from odoo import models, fields


class ThongTinRieng(models.Model):
    _name = "apartment.thong.tin.rieng"
    _description = "Model Thông tin riêng"

    name = fields.Char(string="Tên")
    value = fields.Char(string="Giá trị")
    type_name = fields.Selection(
        string="Tên loại",
        selection=[
            ("a", "a"),
            ("b", "b"),
        ],
    )
    updater = fields.Char(string="Người cập nhật")
    eficiency = fields.Boolean(string="Hiệu lực")
    customer_ids = fields.Many2one(
        string="Khách hàng", comodel_name="apartment.khach.hang"
    )
