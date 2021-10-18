from odoo import api, fields, models
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _name = "sale.order.line.ept"
    _description = "Sale Order Line"

    product_id = fields.Many2one(comodel_name='product.ept', required=True)
    uom_id = fields.Many2one(comodel_name='product.uom.ept', required=True)
    unit_price = fields.Float(string="Unit price", help='Takes unit Price', digits=(6, 2))
    sale_order_id = fields.Many2one(comodel_name='sale.order.ept')
    subtotal_without_tax = fields.Float(string="subtotal without tax", help='Takes subtotal without tax',
                                        digits=(6, 2), compute='_compute_subtotal_without_tax', store=True)

    qty = fields.Integer(string='Qty', help='Takes Qty')

    @api.model
    def create(self, values):
        if values['unit_price'] <= 0:
            raise UserError("Please enter a Unit Price!")
        return super(SaleOrderLine, self).create(values)

    @api.depends('qty', 'product_id.price')
    def _compute_subtotal_without_tax(self):
        for line in self:
            line.subtotal_without_tax = line.qty * line.unit_price
