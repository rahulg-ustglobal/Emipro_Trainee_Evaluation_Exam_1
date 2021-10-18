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
        if values['followup_days'] <= 0:
            raise UserError("Please enter a Follow Up Date!")
        return super(ResPartner, self).create(values)

    def write(self, values):
        if not values:
            if values['followup_days'] <= 0:
                raise UserError("Please enter a Follow Up Date!")
        return super(ResPartner, self).write(values)

    def _compute_visit_count(self):
        for partner in self:
            partner_ids = self.env['field.visit.ept'].search([('partner_id', '=', partner.id)])
            partner.field_visit_count = len(partner_ids.ids)

    def action_view_field_visits(self):
        partner_ids = self.env['field.visit.ept'].search([('partner_id', '=', self.id)])
        view_tree_id = self.env.ref('product_sale_transaction_ept.view_field_visit_tree').id
        view_form_id = self.env.ref('product_sale_transaction_ept.view_field_visit_form').id

        action = {
            'name': _('Field Visits'),
            'type': 'ir.actions.act_window',
            'views': [[view_tree_id, 'tree'], [view_form_id, 'form']],
            'domain': [('id', 'in', partner_ids.ids)],
            'res_model': 'field.visit.ept',
            'view_mode': 'tree,form',
        }
        return action
