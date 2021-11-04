# -*- coding: utf-8 -*-

from odoo import api, models, _, fields
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def update_prices(self):
        self.ensure_one()
        res = super().update_prices()
        for line in self.order_line:
            line.check_discount_limit()
        return res

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_contract = fields.Boolean(related='order_id.pricelist_id.is_contract', store=True)

    @api.onchange('discount')
    def check_discount_limit(self):

        min_margin = self.product_id.min_margin / 100
        
        if self.product_id.min_margin == 100:
            self.discount = 0
            if not self.is_contract:
                message = "This product can't have any discount."
                res = {'warning': {
                    'title': _('Warning'),
                    'message': _(message)
                    }
                }
                return res

        elif not self.env.user.has_group('base.group_system') and self.discount > 0 and\
                (self.margin_percent < min_margin or (self.discount > 10 and not self.is_contract)):

            ##Get maximum discount for margin
            ################################
            discount_margin = (min_margin + (self.purchase_price/self.price_unit) - 1) * (100/(min_margin-1))

            if discount_margin < 0:
                discount_margin = 0

            if discount_margin > 10 and not self.is_contract:
                discount_margin = 10
            
            ##############################
            self.discount = discount_margin
                
            if not self.is_contract:
                message = "You can only assign maximum 10% discount or min margin lower than computed."
                res = {'warning': {
                    'title': _('Warning'),
                    'message': _(message)
                    }
                }
                return res

        if self.margin < 0:
            self.discount = 0

    @api.onchange('product_id', 'price_unit', 'product_uom', 'product_uom_qty', 'tax_id')
    def _onchange_discount(self):
        super()._onchange_discount()
        self.check_discount_limit()
