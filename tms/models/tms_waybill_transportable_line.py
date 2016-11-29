# -*- coding: utf-8 -*-
# © <2012> <Israel Cruz Argil, Argil Consulting>
# © <2016> <Jarsa Sistemas, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class TmsWaybillTransportableLine(models.Model):
    _name = 'tms.waybill.transportable.line'
    _description = 'Shipped Product'
    _order = 'sequence, id desc'

    transportable_id = fields.Many2one(
        'tms.transportable', string='Transportable')
    name = fields.Char('Description', required=True)
    transportable_uom_id = fields.Many2one(
        'product.uom', 'Unit of Measure ', required=True)
    quantity = fields.Float('Quantity (UoM)', requerid=True, default=0.0)
    notes = fields.Char('Notes')
    waybill_id = fields.Many2one(
        'tms.waybill', string='Waybill')
    sequence = fields.Integer(
        'Sequence', help="Gives the sequence order when displaying a list of"
        " sales order lines.", default=10)
    waybill_id = fields.Many2one(
        'tms.waybill', 'waybill', required=False, ondelete='cascade',
        select=True, readonly=True)

    @api.onchange('transportable_id')
    def _onchange_transportable_id(self):
        self.name = self.transportable_id.name
        self.transportable_uom_id = self.transportable_id.uom_id
        factors = []
        for factor in self.waybill_id.customer_factor_ids:
            if factor.factor_type not in [
                    'travel', 'percent', 'qty', 'special']:
                factors.append(factor.factor_type)
                return{
                    'domain': {'transportable_id': [
                        ('factor_type', 'in', (factors))]}
                }
