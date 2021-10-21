from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _name = "res.partner.ept"
    _description = "Res Partner"

    name = fields.Char(string='Partner Name', help='Takes Partner Name', required=True)
    next_visit_date = fields.Date(string='Next Visit Date', help='Takes next visit date')
    followup_days = fields.Integer(string='Next Followup days', help='Takes Followup days')
    field_visit_count = fields.Integer(string='Field Visit Count', help='Takes field visit count',
                                       compute='_compute_visit_count', store=False)

    @api.model
    def create(self, values):
        """
        :param values: This values is the parameter of the create method,
                       It will accept the values in the the form of dictionary
        :return: It is returning the super statement.
        :self : This is called as browse object
        UserError : This is the validation which is checking the values of
                    the followup_days which is less than or equal to the zero then
                    generate the User validation error as follows.
        """
        if values['followup_days'] <= 0:
            raise UserError("Please enter a Follow Up Date!")
        return super(ResPartner, self).create(values)

    def write(self, values):
        """
        :param values: This values is the parameter of the write method,
                       It will accept the values in the the form of currently updated values.
        :return: It is returning the super statement.
        :self : This is called as browse object
        UserError : This is the validation which is checking the values of
                    the followup_days which is less than or equal to the zero then
                    generate the User validation error as follows.
        """
        if not values:
            if values['followup_days'] <= 0:
                raise UserError("Please enter a Follow Up Date!")
        return super(ResPartner, self).write(values)

    def _compute_visit_count(self):
        """
        field_visit_count: This is the field which is compute field and the compute field name is
                           _compute_visit_count which will calculate the visit_count which the help of
                           compute field.
        :return: Nothing to return.
        self : self is the object and we are iterating it with the help of for loop for getting the partner_id.
        and with adding the domain with the search method given as follows.
        """
        for partner in self:
            partner_ids = self.env['field.visit.ept'].search([('partner_id', '=', partner.id)])
            partner.field_visit_count = len(partner_ids.ids)

    def action_view_field_visits(self):
        """
        action_view_field_visits : This is the object type of button button box which is created because we have to
                                   show the list and form view according to the condition.
        partner_ids : This is the variable which is used to store the partner Id using domain with search method.
        view_tree_id : This is the tree view id which store the tree view id with getting the reference with
                      module_name.tree_view_xml_id.
        view_form_id : This is the form view id which store the form view id with getting the reference with
                      module_name.form_view_xml_id.
        action : this is the user defined/created dictionary for getting the fields of the xml file.
        :return: at last returning the action after getting the user defined dictionary.
        """
        partner_ids = self.env['field.visit.ept'].search([('partner_id', '=', self.id)]).ids
        view_tree_id = self.env.ref('product_sale_transaction_ept.view_field_visit_tree').id
        view_form_id = self.env.ref('product_sale_transaction_ept.view_field_visit_form').id

        action = {
            'name': _('Field Visits'),
            'type': 'ir.actions.act_window',
            'res_model': 'field.visit.ept'
        }
        ##--------------------------------------------------------##

        if len(partner_ids) > 1:
            action.update({
                'view_mode': 'tree,form',
                'views': [(view_tree_id, 'tree'), (view_form_id, 'form')],
                'domain': [('id', 'in', partner_ids)]
            })
        elif len(partner_ids) == 1:
            action.update({
                'view_mode': 'form',
                'views': [[view_form_id, 'form']],
                'res_id': partner_ids[0]
            })
        else:
            raise UserError("Field Visits Is Empty!!")
        return action
        ##--------------------------------------------------------##

    ##--------------------------------------------------------##
    # def action_view_field_visits(self):
    #     partner_ids = self.env['field.visit.ept'].search([('partner_id', '=', self.id)])
    #     view_tree_id = self.env.ref('product_sale_transaction_ept.view_field_visit_tree').id
    #     view_form_id = self.env.ref('product_sale_transaction_ept.view_field_visit_form').id
    #
    #     action = {
    #         'name': _('Field Visits'),
    #         'type': 'ir.actions.act_window',
    #         'views': [[view_tree_id, 'tree'], [view_form_id, 'form']],
    #         'domain': [('id', 'in', partner_ids.ids)],
    #         'res_model': 'field.visit.ept',
    #         'view_mode': 'tree,form',
    #     }
    #     return action
    ##--------------------------------------------------------##
    # def action_delivery_order(self):
    #     pickings = self.picking_ids.ids
    #     view_id = self.env.ref('sale_ept.view_stock_picking_tree').id
    #     view_form_id = self.env.ref('sale_ept.view_stock_picking_form').id
    #     action = {
    #         'type': 'ir.actions.act_window',
    #         'name': _('Delivery Order'),
    #         'res_model': 'stock.picking.ept',
    #     }
    #     if len(pickings) == 1:
    #         action.update({
    #             'view_mode': 'form',
    #             'views': [[view_form_id, 'form']],
    #             'res_id': pickings[0]
    #         })
    #     else:
    #         action.update({
    #             'view_mode': 'tree,form',
    #             # 'views': [[view_id, 'tree']],
    #             'views': [(view_id, 'tree'), (view_form_id, 'form')],
    #             'domain': [('sale_order_id', 'in', [self.id])],
    #         })
    #     return action
