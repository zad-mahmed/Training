from odoo import models, fields, api, _


class PurchaseRequest(models.Model):
    _name = 'purchase.request'
    _description = "Purchase Request"

    request_name = fields.Char(required=True)
    requested_by = fields.Many2one('res.users', required=True, default=lambda self: self.env.user.id)
    start_date = fields.Date('Start date', required=True,  default=fields.Date.context_today)
    end_date = fields.Date()
    rejection_reason = fields.Char(readonly=1)
    order_lines_ids = fields.One2many('purchase.request.lines', 'pur_req_id')
    total_price = fields.Float(compute='compute_total_price')
    state = fields.Selection([('draft', 'Draft'),
                               ('to_be_approved', 'To be approved'),
                               ('approved', 'Approved'),
                               ('reject', 'Reject'),
                               ('cancel', 'Cancel')], default='draft')

    def compute_total_price(self):
        for rec in self:
            rec.total_price = sum(rec.order_lines_ids.mapped('total'))
            if rec.total_price == 0.0:
                rec.total_price = 0.0

    def action_to_be_approved(self):
        for rec in self:
            print("inside to_be_approved action")
            rec.state = 'to_be_approved'
            # rec.write({
            #     'state': 'draft'
            # })

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    def action_approve(self):
        for rec in self:
            rec.state = 'approved'
        full_mail = (_('Purchase Request (%s) has been approved  approval by %s')
                     % (self.request_name, self.env.user.name))
        users = self.env.ref('test_project.purchase_manger_group').users
        for user in users:
            mail_values = {
                'auto_delete': True,
                'author_id': self.env.user.partner_id.id,
                'email_from': self.env.user.partner_id.email_formatted,
                'email_to': user.partner_id.email_formatted,
                'body_html': full_mail,
                'subject': full_mail,
            }
            print(mail_values)
            mail = self.env['mail.mail'].sudo().create(mail_values)
            mail.sudo().send()

    def action_reject(self):
        for rec in self:
            rec.state = 'reject'

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_open_rejection_wizard(self):
        for rec in self:
            rec.state = 'reject'
        return {
            'name': 'Rejection Reason',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'rejection.wizard',
            'target': 'new',
            'context': self.env.context
        }


class PurchaseRequestLines(models.Model):
    _name = 'purchase.request.lines'

    product_id = fields.Many2one('product.product', required=True)
    pur_req_id = fields.Many2one('purchase.request')
    description = fields.Char(related='product_id.name')
    quantity = fields.Float(default='1.0')
    total = fields.Float(readonly=1, compute='_compute_total')
    cost_price = fields.Float(readonly=1, related='product_id.list_price')

    @api.depends('quantity', 'cost_price')
    def _compute_total(self):
        for rec in self:
            rec.total = rec.quantity * rec.cost_price

