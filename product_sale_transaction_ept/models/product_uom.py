from odoo import api, fields, models


class ProductUom(models.Model):
    _name = "product.uom.ept"
    _description = "Product Uom"

    name = fields.Char(string='product Uom Name', help="Takes product Uom Name", required=True)