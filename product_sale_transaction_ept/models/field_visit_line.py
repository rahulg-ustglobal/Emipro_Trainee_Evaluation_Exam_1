from odoo import api, fields, models
from odoo.exceptions import UserError


class FieldVisitLine(models.Model):
    _name = "field.visit.line.ept"
    _description = "Field Visit Line"

    field_visit_id = fields.Many2one(comodel_name='field.visit.ept', string="Field Visit")
    product_id = fields.Many2one(comodel_name='product.ept', string="Product")
    uom_id = fields.Many2one(comodel_name='product.uom.ept', string="Uom ID")
    qty = fields.Integer(string='Qty', help='Takes Qty')

    @api.model
    def create(self, values):
        """
        :param values: This values is the parameter of the create method,
                     It will accept the values in the the form of dictionary
        :return: It is returning the super statement.
        :self : This is called as browse object
        UserError : This is the validation which is checking the values of
                    the quantity which is less than or equal to the zero then
                    generate the User validation error as follows.
        """
        if values['qty'] <= 0:
            raise UserError("Please enter a Quantity!")
        return super(FieldVisitLine, self).create(values)
