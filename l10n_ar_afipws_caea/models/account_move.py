from odoo import fields, models, _
from odoo.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    caea_id = fields.Many2one(
        'afipws.caea',
        string='Caea',
    )

    def do_pyafipws_request_cae(self):
        caea_state = self.env['ir.config_parameter'].get_param('afip.ws.caea.state', 'inactive')
        _logger.info('caea_state %r' % caea_state)
        if caea_state == 'inactive':
            return super(AccountMove, self).do_pyafipws_request_cae()
        elif caea_state == 'active':

            for inv in self:
                # Ignore invoices with cae (do not check date)
                if inv.afip_auth_code:
                    continue

                afip_ws = inv.journal_id.afip_ws
                if not afip_ws:
                    continue

                # Ignore invoice if not ws on point of sale
                if not afip_ws:
                    raise UserError(_(
                        'If you use electronic journals (invoice id %s) you need '
                        'configure AFIP WS on the journal') % (inv.id))

                active_caea = inv.company_id.get_active_caea()
                # if no validation type and we are on electronic invoice, it means
                # that we are on a testing database without homologation
                # certificates
                if len(active_caea):
                    msg = (
                        _('Afip conditional validation (CAEA %s)') % active_caea.afip_caea)
                    inv.write({
                        'afip_auth_mode': 'CAEA',
                        'afip_auth_code': active_caea.afip_caea,
                        'afip_auth_code_due': inv.invoice_date,
                        'afip_result': '',
                        'afip_message': msg,
                        'caea_id': active_caea.id
                    })
                    inv.message_post(body=msg)
                    continue
                else:
                    raise UserError(_('The company does not have active CAEA'))
        elif caea_state == 'syncro':
            #to-do filter and raise}
            _logger.info('aca')
            return super(AccountMove, self).do_pyafipws_request_cae()
