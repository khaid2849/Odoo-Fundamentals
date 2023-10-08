from datetime import datetime
from odoo import models, fields, api


class NganhNghe(models.Model):
    _name = "apartment.nganh.nghe"
    _description = "Model Ngành nghề"

    code = fields.Char(string="Mã")
    name = fields.Char(string="Tên")
    description = fields.Text(string="Ghi chú")
    updater = fields.Char(string="Người cập nhật")

    @api.depends("write_date")
    def _compute_write_date(self):
        for record in self:
            write_date = record.write_date
            if write_date:
                record.write_date = write_date.strftime("%d/%M/%Y, %H:%M:%S")

    @api.model
    def create(self, vals):
        vals["code"] = self.env["ir.sequence"].next_by_code(
            "apartment.nganh.nghe.sequence"
        ) or _("New")

        res = super(NganhNghe, self).create(vals)
        return res

    _sql_constraints = [
        ("uniq_name", "unique(ma)", "Mã phải là duy nhất "),
    ]
