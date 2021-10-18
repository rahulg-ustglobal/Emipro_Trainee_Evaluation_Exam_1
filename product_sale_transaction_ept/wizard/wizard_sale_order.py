from odoo import models, fields, api


class SaleOrder(models.TransientModel):
    _name = "sale.order.tre"
    _description = "Sale Order"

    def action_product_stock(self):
        field_visit = self.env['field.visit.ept'].browse(self._context.get('active_id'))
        sale_order_line_list = list()
        for field_line in field_visit.field_visit_line_ids:
            sale_order_line_values = {
                'product_id': field_line.product_id.id,
                'uom_id': field_line.uom_id.id,
                'unit_price': field_line.product_id.price,
                'qty': field_line.qty,
            }
            sale_order_line_list.append((0, 0, sale_order_line_values))

        sale_order_values = {
            'partner_id': field_visit.partner_id.id,
            'order_date': field_visit.visit_date,
            'order_line_ids': sale_order_line_list,
        }
        self.env['sale.order.ept'].create(sale_order_values)
