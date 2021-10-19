from odoo import api, fields, models
from odoo.exceptions import UserError


class Product(models.Model):
    _name = "product.ept"
    _description = "Product Model"

    name = fields.Char(string='Product Name', help="Takes Product Name", required=True)
    price = fields.Float(string="Product Price", help='Takes Product Price', digits=(6, 2), required=True)
    product_sku = fields.Char(string='Product Sku', help='Takes Product Sku', required=True)
    uom_id = fields.Many2one(comodel_name='product.uom.ept',string="Uom ID")

    @api.model
    def create(self, values):
        """
        :param values: This values is the parameter of the create method,
                       It will accept the values in the the form of dictionary
        :return: It is returning the super statement.
        :self : This is called as browse object
        UserError : This is the validation which is checking the values of
                    the price which is less than or equal to the zero then
                    generate the User validation error as follows.
        """
        if values['price'] <= 0:
            raise UserError("Please enter a price!")
        return super(Product, self).create(values)

    # @api.model
    def write(self, values):
        """
        :param values: This values is the parameter of the write method,
                       It will accept the values in the the form of updated values.
        :return: It is returning the super statement.
        :self : This is called as browse object
        UserError : This is the validation which is checking the values of
                    the price which is less than or equal to the zero then
                    generate the User validation error as follows.
        """

        if values['price'] <= 0:
            raise UserError("Please enter a price!")
        return super(Product, self).write(values)

