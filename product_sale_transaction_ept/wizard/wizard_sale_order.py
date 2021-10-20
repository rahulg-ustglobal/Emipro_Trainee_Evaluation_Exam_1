from odoo import models, fields, api


class SaleOrder(models.TransientModel):
    _name = "sale.order.tre"
    _description = "Sale Order"

    ##---------------------------------------------------------------##

    name = fields.Char(string='Field Visit', help="Takes Field Visit", required=True, default='New Visit',
                       readonly=True)

    @api.model
    def default_get(self, fields):
        res = super(SaleOrder, self).default_get(fields)
        field_visit = self.env['field.visit.ept'].browse(self._context.get('active_id'))

        res.update({
            'name': field_visit.name
        })
        return res

    ##---------------------------------------------------------------##

    def action_product_stock(self):
        """
        action_product_stock : This is the action which is used to show the product stock...and it
                               is the wizard which will generate the sale order using button which having the
                               object type and getting the sale_order_values....and will generate the order...
        active_id : This is the active id which is store the id of the current active record...
        sale_order_line_list : This will store the sale order line in the from of list...
        sale_order_values : This is the sale order values in the form of dictionary...
        """
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
