# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full licensing details.

from odoo import fields, models


class Form(models.Model):
    _inherit = 'formio.form'

    crm_lead_id = fields.Many2one(
        "crm.lead", string="CRM Lead", readonly=True, ondelete="cascade"
    )

    def _prepare_create_vals(self, vals):
        vals = super(Form, self)._prepare_create_vals(vals)
        builder = self._get_builder_from_id(vals.get('builder_id'))
        res_id = self._context.get('active_id')
        
        if not res_id :
            if not builder.res_model_id.model == 'crm.lead' or not builder:
                return vals
 
            uid = self._context.get('uid')   

            # Could Also Set the Team here
            new_lead = self.env['crm.lead'].sudo().create({
                'name': self.env["formio.builder"].browse(vals.get('builder_id')).title,
		        'formio_forms': [(4, self.id)], 
                'user_id': self.env["formio.builder"].browse(vals.get('builder_id')).create_uid.id,
                'partner_id': self.env['res.users'].browse(uid).partner_id.id,
            })
            res_id = new_lead.id


        lead = self.env['crm.lead'].browse(res_id)
        action = self.env.ref('crm.crm_case_tree_view_oppor')
        url = '/web?#id={id}&view_type=form&model={model}&action={action}'.format(
            id=res_id,
            model='crm.lead',
            action=action.id)
        vals['crm_lead_id'] = res_id
        vals['res_partner_id'] = lead.partner_id.id
        vals['res_act_window_url'] = url
        vals['res_name'] = lead.name
        return vals

    def _get_builder_id_domain(self):
        self.ensure_one()
        domain = super()._get_builder_id_domain()
        if self._context.get('active_model') == 'crm.lead':
            res_model_id = self.env.ref('crm.model_crm_lead').id
            domain.append(('res_model_id', '=', res_model_id))
        return domain
