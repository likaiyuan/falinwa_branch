# -*- coding: utf-8 -*-
# Falinwa Hans
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#
# -*- coding: utf-8 -*-
from openerp import fields, models, api
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class stock_location_route(models.Model):
    _name = "stock.location.route"
    _inherit = "stock.location.route"
    
    fal_check_stock = fields.Boolean('Check Stock')
    
#end of stock_location_route()

class stock_move(models.Model):
    _name = "stock.move"
    _inherit = "stock.move"
    
    @api.model
    def _prepare_procurement_from_move(self, move):
        res = super(stock_move, self)._prepare_procurement_from_move(move)
        #print move.rule_id.name
        #print move.rule_id.route_id.fal_check_stock
        #print 'sad'
        #print move.route_ids
        #print [(x.fal_check_stock) for x in move.route_ids]
        if move.rule_id.route_id.fal_check_stock or True in [(x.fal_check_stock) for x in move.route_ids]:
            if move.product_id.virtual_available >= 0:
                res['product_qty'] = move.product_uom_qty - move.product_id.virtual_available
                res['name'] += _(" The quantity of order is: %s , but Forescasted Quantity for this product is: %s , so we automatically adjust it to: %s") % (move.product_uom_qty, move.product_id.virtual_available, res['product_qty'])
            if move.product_uom_qty <= move.product_id.virtual_available:
                res['state'] = 'cancel'
        return res
        
#end of stock_move


class mrp_production(models.Model):
    _name = "mrp.production"
    _inherit = "mrp.production"        
    
    @api.model
    def _make_consume_line_from_data(self, production, product, uom_id, qty, uos_id, uos_qty):
        res = super(mrp_production, self)._make_consume_line_from_data(production, product, uom_id, qty, uos_id, uos_qty)
        self.env['stock.move'].browse(res).write({'route_ids': [(4, x.id) for x in product.route_ids],})
        return res
        
#end of mrp_production