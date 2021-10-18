from odoo import api, fields, models


class SaleOrder(models.Model):
    _name = "sale.order.ept"
    _description = "Sale Order"

    name = fields.Char(string='product Name', help="Takes Product Name", required=True, default='New')
    partner_id = fields.Many2one(comodel_name='res.partner.ept', required=True)
    order_date = fields.Date(string='Order Date', help='Takes Order date', required=True)

    order_line_ids = fields.One2many(comodel_name='sale.order.line.ept',inverse_name='sale_order_id',
                                     string="Order Line")
    order_total = fields.Float(string="Order Total", help='Takes Order Total', digits=(6, 2),
                               compute='_compute_order_total', store=True)

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('sale.order.ept') or ('New')
        return super(SaleOrder, self).create(vals)

    @api.depends('order_line_ids')
    def _compute_order_total(self):
        order_total = 0
        for order_line in self.order_line_ids:
            order_total += order_line.subtotal_without_tax
        self.order_total = order_total
