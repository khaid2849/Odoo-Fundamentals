from odoo import models, fields, api


class NganhNghe(models.Model):
    _name = "apartment.nganh.nghe"
    _description = "Model Ngành nghề"

    code = fields.Char(string="Mã", required=True)
    name = fields.Char(string="Tên", required=True)
    description = fields.Text(string="Ghi chú")
    active = fields.Boolean(default=False)

    @api.depends("write_date")
    def _compute_write_date(self):
        for record in self:
            write_date = record.write_date
            if write_date:
                record.write_date = write_date.strftime("%d/%M/%Y, %H:%M:%S")

    _sql_constraints = [
        ("uniq_name", "unique(ma)", "Mã phải là duy nhất "),
    ]
