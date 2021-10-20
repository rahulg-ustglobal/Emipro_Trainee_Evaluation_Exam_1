from odoo import api, fields, models
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _name = "sale.order.line.ept"
    _description = "Sale Order Line"

    product_id = fields.Many2one(comodel_name='product.ept', required=True)
    uom_id = fields.Many2one(comodel_name='product.uom.ept', required=True)
    unit_price = fields.Float(string="Unit price", help='Takes unit Price', digits=(6, 2))
    sale_order_id = fields.Many2one(comodel_name='sale.order.ept')
    subtotal_without_tax = fields.Float(string="Subtotal Without Tax", help='Takes subtotal without tax',
                                        digits=(6, 2), compute='_compute_subtotal_without_tax', store=True)

    qty = fields.Integer(string='Qty', help='Takes Qty')

    @api.model
    def create(self, values):
        """
        :param values: This values is the parameter of the create method,
                       It will accept the values in the the form of dictionary
        :return: It is returning the super statement.
        :self : This is called as browse object
        UserError : This is the validation which is checking the values of
                    the unit_price which is less than or equal to the zero then
                    generate the User validation error as follows.
        """
        if values['unit_price'] <= 0:
            raise UserError("Please enter a Unit Price!")
        return super(SaleOrderLine, self).create(values)

    @api.depends('qty', 'product_id.price')
    def _compute_subtotal_without_tax(self):
        """
        _compute_subtotal_without_tax : This is the compute method which is created for calculating the
                                        subtotal_without_tax...This method is depends on the two fields like
                                        qty and product_id.price...after that we are iterating the self for
                                        getting the lines from the self for calculating the subtotal_without_tax..
                                        we will get qty and unit_price using iterating...
        :return: Nothing to return
        """
        for line in self:
            line.subtotal_without_tax = line.qty * line.unit_price
