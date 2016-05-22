'''
Created on 05/08/2015

@author: alconor
'''
from openerp.osv import fields, osv, orm
from datetime import date, datetime
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

class fleet_vehicle(osv.osv):
    _inherit = 'fleet.vehicle'
    _columns = {
               'orometer_unit' : fields.selection([('horas','Horas'),('minutos','Minutos')], 'Orometer Unit', help='Unit of the orometer ',required=False),
               'odometer_unit': fields.selection([('kilometers', 'Kilometers'),('miles','Miles'),('hours','Hours')], 'Odometer Unit', help='Unit of the odometer ',required=True),               
               }
    #fleet_vehicle()

class fleet_vehicle_log_fuel(osv.osv):
    _inherit = 'fleet.vehicle.log.fuel' 
    _columns = {
                'liter': fields.float('Liter',digits=(12,5)),
                'price_per_liter': fields.float('Price Per Liter',digits=(12,5))
                }
    #fleet_vehicle_log_fuel()
    # La precision decimal se gestiona en la el menu de Estructura de datos\ Precision de Moneda
    def on_change_liter(self, cr, uid, ids, liter, price_per_liter, amount, context=None):
        #need to cast in float because the value receveid from web client maybe an integer (Javascript and JSON do not
        #make any difference between 3.0 and 3). This cause a problem if you encode, for example, 2 liters at 1.5 per
        #liter => total is computed as 3.0, then trigger an onchange that recomputes price_per_liter as 3/2=1 (instead
        #of 3.0/2=1.5)
        #If there is no change in the result, we return an empty dict to prevent an infinite loop due to the 3 intertwine
        #onchange. And in order to verify that there is no change in the result, we have to limit the precision of the 
        #computation to 2 decimal
        liter = float(liter)
        price_per_liter = float(price_per_liter)
        amount = float(amount)
        if liter > 0 and price_per_liter > 0 and round(liter*price_per_liter,2) != amount:
            return {'value' : {'amount' : round(liter * price_per_liter,2),}}
        elif amount > 0 and liter > 0 and round(amount/liter,5) != price_per_liter:
            return {'value' : {'price_per_liter' : round(amount / liter,5),}}
        elif amount > 0 and price_per_liter > 0 and round(amount/price_per_liter,5) != liter:
            return {'value' : {'liter' : round(amount / price_per_liter,5),}}
        else :
            return {}
    def on_change_price_per_liter(self, cr, uid, ids, liter, price_per_liter, amount, context=None):
        #need to cast in float because the value receveid from web client maybe an integer (Javascript and JSON do not
        #make any difference between 3.0 and 3). This cause a problem if you encode, for example, 2 liters at 1.5 per
        #liter => total is computed as 3.0, then trigger an onchange that recomputes price_per_liter as 3/2=1 (instead
        #of 3.0/2=1.5)
        #If there is no change in the result, we return an empty dict to prevent an infinite loop due to the 3 intertwine
        #onchange. And in order to verify that there is no change in the result, we have to limit the precision of the 
        #computation to 2 decimal
        liter = float(liter)
        price_per_liter = float(price_per_liter)
        amount = float(amount)
        if liter > 0 and price_per_liter > 0 and round(liter*price_per_liter,2) != amount:
            return {'value' : {'amount' : round(liter * price_per_liter,2),}}
        elif amount > 0 and price_per_liter > 0 and round(amount/price_per_liter,5) != liter:
            return {'value' : {'liter' : round(amount / price_per_liter,5),}}
        elif amount > 0 and liter > 0 and round(amount/liter,5) != price_per_liter:
            return {'value' : {'price_per_liter' : round(amount / liter,5),}}
        else :
            return {}

    def on_change_amount(self, cr, uid, ids, liter, price_per_liter, amount, context=None):
        #need to cast in float because the value receveid from web client maybe an integer (Javascript and JSON do not
        #make any difference between 3.0 and 3). This cause a problem if you encode, for example, 2 liters at 1.5 per
        #liter => total is computed as 3.0, then trigger an onchange that recomputes price_per_liter as 3/2=1 (instead
        #of 3.0/2=1.5)
        #If there is no change in the result, we return an empty dict to prevent an infinite loop due to the 3 intertwine
        #onchange. And in order to verify that there is no change in the result, we have to limit the precision of the 
        #computation to 2 decimal
        liter = float(liter)
        price_per_liter = float(price_per_liter)
        amount = float(amount)
        if amount > 0 and liter > 0 and round(amount/liter,5) != price_per_liter:
            return {'value': {'price_per_liter': round(amount / liter,5),}}
        elif amount > 0 and price_per_liter > 0 and round(amount/price_per_liter,5) != liter:
            return {'value': {'liter': round(amount / price_per_liter,5),}}
        elif liter > 0 and price_per_liter > 0 and round(liter*price_per_liter,2) != amount:
            return {'value': {'amount': round(liter * price_per_liter,2),}}
        else :
            return {}


class anexos_conceptos_pa(osv.osv):
    _name = 'anexos.conceptos.pa'
    _description = 'Formulario de Conceptos para Anexos Fiscales de Panama v1.2'
    _columns = {
              'name' : fields.char('Nombre del Concepto',size=256,required=True,help='Descripcion del Nombre del Concepto'),
              'concepto' : fields.char('Concepto',size=2,required=True),
              'codigo_tipo_pago' : fields.selection([('0','COMPRAS'),('1','OTROS COSTOS'),('2','OTROS GASTOS'),('3','GASTOS MEDICOS')],'Codigo Tipo Pago',required=True),
              'anexo' : fields.char('Anexo',size=3,required=True),
              #'partner_id' : fields.many2many('res_partner','res_partner_anexos_conceptos_pa_rel','concepto', 'partner_id','Partner', store=True, readonly=False)
               }
    #anexos_conceptos_pa()
    
class res_partner(osv.osv):
    _inherit = "res.partner"
    _columns = {
                # RUC: Registro Unico del Contribuyente (Panama)
                'ruc': fields.char('RUC', size=45),
                # DV: Digito verificador
                'dv': fields.char('DV', size=2),
                # TIPO_PERSONA
                #  1=NATURAL 
                #  2=JURIDICO
                #  3=OTROS
                #  4=EXTRANJERO
                'tipo_persona': fields.selection([('1','NATURAL'),('2','JURIDICO'),('3','OTROS'),('4','EXTRANJERO')],'Tipo Persona',required=True),
                # Concepto Varios a Uno
                #'concepto' : fields.many2one('anexos.conceptos.pa', 'concepto','Anexo Concepto', store=True, readonly=False)
                'concepto' : fields.many2many('anexos.conceptos.pa','res_partner_anexos_conceptos_pa_rel','partner_id', 'concepto','Concepto de Anexo', store=True, readonly=False)
               }
    #res_partner()
    
class account_invoice_line(osv.osv):
    _inherit = "account.invoice.line" 
    _columns = {
                # CONCEPTO DE ANEXO
                #'concepto' : fields.one2many('anexos.conceptos.pa', 'concepto','Anexo Concepto', store=True, readonly=False)
                'concepto' : fields.many2many('anexos.conceptos.pa',
                                              'account_invoice_line_anexos_conceptos_pa_rel',
                                              'invoice_line_id',
                                              'concepto',
                                              'Concepto de Anexo',
                                              store=True,
                                              readonly=False)
                
                }
    #account_invoice_line()

def product_id_change2(self, product, uom_id, qty=0, name='', type='out_invoice',
        partner_id=False, fposition_id=False, price_unit=False, currency_id=False,
        company_id=None):
    context = self._context
    company_id = company_id if company_id is not None else context.get('company_id', False)
    self = self.with_context(company_id=company_id, force_company=company_id)

    if not partner_id:
        raise except_orm(_('No Partner Defined!'), _("You must first select a partner!"))
    if not product:
        if type in ('in_invoice', 'in_refund'):
            return {'value': {}, 'domain': {'product_uom': []}}
        else:
            return {'value': {'price_unit': 0.0}, 'domain': {'product_uom': []}}

    values = {}

      
    part = self.env['res.partner'].browse(partner_id)
    fpos = self.env['account.fiscal.position'].browse(fposition_id)

    if part.lang:
        self = self.with_context(lang=part.lang)
        
    values['concepto'] = part.concepto
    product = self.env['product.product'].browse(product)

    values['name'] = product.partner_ref
    if type in ('out_invoice', 'out_refund'):
        account = product.property_account_income or product.categ_id.property_account_income_categ
    else:
        account = product.property_account_expense or product.categ_id.property_account_expense_categ
    account = fpos.map_account(account)
    if account:
        values['account_id'] = account.id

    if type in ('out_invoice', 'out_refund'):
        taxes = product.taxes_id or account.tax_ids
        if product.description_sale:
            values['name'] += '\n' + product.description_sale
    else:
        taxes = product.supplier_taxes_id or account.tax_ids
        if product.description_purchase:
            values['name'] += '\n' + product.description_purchase

    taxes = fpos.map_tax(taxes)
    values['invoice_line_tax_id'] = taxes.ids

    if type in ('in_invoice', 'in_refund'):
        values['price_unit'] = price_unit or product.standard_price
    else:
        values['price_unit'] = product.lst_price

    values['uos_id'] = uom_id or product.uom_id.id
    domain = {'uos_id': [('category_id', '=', product.uom_id.category_id.id)]}

    company = self.env['res.company'].browse(company_id)
    currency = self.env['res.currency'].browse(currency_id)

    if company and currency:
        if company.currency_id != currency:
            if type in ('in_invoice', 'in_refund'):
                values['price_unit'] = product.standard_price
            values['price_unit'] = values['price_unit'] * currency.rate

        if values['uos_id'] and values['uos_id'] != product.uom_id.id:
            values['price_unit'] = self.env['product.uom']._compute_price(
                product.uom_id.id, values['price_unit'], values['uos_id'])

    return {'value': values, 'domain': domain}
