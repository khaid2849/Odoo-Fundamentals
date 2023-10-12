from odoo import models, fields, api


class DichVu(models.Model):
    _name = "apartment.dich.vu"
    _description = "Model Dịch vụ"

    code = fields.Char(string="Mã", required=True)
    name = fields.Char(string="Tên", required=True)
    provider = fields.Many2one(string="Nhà cung cấp", comodel_name="apartment.nha.cung.cap", required=True)
    description = fields.Char(string="Ghi chú")
    company_id = fields.Many2one(comodel_name="res.company", string='Company', index=True)
    currency_id = fields.Many2one(comodel_name="res.currency", string='Currency', compute='_compute_currency_id')
    price = fields.Float(string="Đơn giá", required=True)
    uom = fields.Many2one(string="Đơn vị tính", comodel_name="uom.uom", required=True)
    tax_id = fields.Many2many(
        comodel_name="account.tax",
        string="Thuế",
        domain=[("type_tax_use", "=", "sale")])
    product_id = fields.Many2one(comodel_name="product.template")
    active = fields.Boolean()

    @api.depends("write_date")
    def _compute_write_date(self):
        for service in self:
            write_date = service.write_date
            if write_date:
                service.write_date = write_date.strftime("%d/%M/%Y, %H:%M:%S")

    @api.depends('company_id')
    def _compute_currency_id(self):
        main_company = self.env['res.company']._get_main_company()
        for service in self:
            service.currency_id = service.company_id.sudo().currency_id.id or main_company.currency_id.id

    @api.model
    def create(self, vals):
        product_vals = {
            "name": vals.get("name"),
            "type": "service",
            "currency_id": vals.get("currency_id"),
            "company_id": vals.get("company_id"),
            "uom_id": vals.get("uom"),
        }
        product = self.env["product.template"].create(product_vals)
        vals["product_id"] = product.id
        return super(DichVu, self).create(vals)

    @api.onchange('code')
    def onchange_code(self):
        res = {}
        if self.code:
            self.code = ""
            res['warning'] = {'title': 'Warning', 'message': 'Your Message Here.'}
            return res
