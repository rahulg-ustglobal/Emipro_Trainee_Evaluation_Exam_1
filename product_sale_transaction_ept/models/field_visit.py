from odoo import api, fields, models
import datetime
from odoo.exceptions import UserError


class FieldVisit(models.Model):
    _name = "field.visit.ept"
    _description = "Field Visit"

    name = fields.Char(string='product Name', help="Takes Product Name", required=True, default='New Visit')
    user_id = fields.Many2one(comodel_name='res.users', string="User ID",
                              help="This field will accept the User ID")
    partner_id = fields.Many2one(comodel_name='res.partner.ept')
    field_visit_line_ids = fields.One2many(comodel_name='field.visit.line.ept', inverse_name='field_visit_id')
    visit_date = fields.Date(string='Visit Date', help='Takes visit date', default=fields.date.today())
    state = fields.Selection([('Draft', 'Draft'), ('Completed', 'Completed'), ('Cancel', 'Cancel')],
                             default='Draft', string="Status", required=True)
    visit_log = fields.Text(string='Visit Log', help='Takes visit log')

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('field.visit.ept') or ('New')
        return super(FieldVisit, self).create(vals)

    def write(self, vals):
        if vals:
            if 'visit_log' in vals.keys():
                if self.state == 'Completed' and vals['visit_log'] == '':
                    raise UserError("Please enter value in visit log")

        return super(FieldVisit, self).write(vals)

    def action_complete(self):
        visit_date = self.visit_date
        partner = self.partner_id
        partner.next_visit_date = visit_date + datetime.timedelta(days=partner.followup_days)
        self.write({
            'visit_log': 'This Visit is Completed.',
            'state': 'Completed'
        })
