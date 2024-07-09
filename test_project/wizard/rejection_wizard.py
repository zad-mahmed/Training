from odoo import models, fields


class RejectionWizard(models.TransientModel):
    _name = 'rejection.wizard'
    _description = 'Rejection Reason Wizard'

    rejection_reason = fields.Text(string="Rejection Reason", required=True)

    def action_confirm_rejection(self):
        active_id = self.env.context.get('active_id')
        request = self.env['purchase.request'].browse(active_id)
        if request:
            request.write({
                'rejection_reason': self.rejection_reason
            })
        return {'type': 'ir.actions.act_window_close'}
