#This file is part sale_contact module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.model import fields
from trytond.pyson import Eval

__all__ = ['Sale']
__metaclass__ = PoolMeta

_STATES = {
    'readonly': Eval('state') != 'draft',
}
_DEPENDS = ['state']


class Sale:
    __name__ = 'sale.sale'
    contact_address = fields.Many2One('party.address', 'Contact Address',
        states=_STATES, depends=['state', 'party'],
        domain=[('party', '=', Eval('party'))])

    def on_change_party(self):
        changes = super(Sale, self).on_change_party()

        changes['contact_address'] = None
        if self.party:
            contact_address = self.party.address_get(type='contact')
            if contact_address:
                changes['contact_address'] = contact_address.id
                changes['contact_address.rec_name'] = contact_address.rec_name
        return changes

    def _get_invoice_sale(self, invoice_type):
        invoice = super(Sale, self)._get_invoice_sale(invoice_type)

        if self.contact_address:
            invoice.contact_address = self.contact_address
        else:
            contact_address = invoice.party.address_get(type='contact')
            if contact_address:
                invoice.contact_address = contact_address

        return invoice
