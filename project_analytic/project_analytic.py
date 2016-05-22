'''
Created on 05/08/2015

@author: alconor
'''
from openerp.osv import fields, osv, orm
from datetime import date, datetime
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

class project_phase(osv.osv):
    _inherit = "project.phase"
    _columns = {
                'codigo_phase_id' : fields.char('Codigo fase ID',size=15,required=True)
                }
    #project_phase()
     
# Agrega a la linea de la factura el campo phase_id  
class account_invoice_line(osv.osv):
    _inherit = "account.invoice.line" 
    _columns = {
                # CONCEPTO DE ANEXO
                #'concepto' : fields.one2many('anexos.conceptos.pa', 'concepto', 'Anexo Concepto', store=True, readonly=False),
                # PHASE ID DE PROYECTO
                #'codigo_phase_id' : fields.one2many('project.phase'      , 'codigo_phase_id', 'Project Phases', store=True, readonly=False)
                #'codigo_phase_id' : fields.many2one('project.phase'      , 'Project Phase', ondelete='cascade', required=True),
                'codigo_phase_id' : fields.many2many('project.phase',
                                              'account_invoice_line_project_phase_rel',
                                              'invoice_line_id',
                                              'codigo_phase_id',
                                              'Fase de Proyecto',
                                              store=True,
                                              readonly=False),
                'codigo_categoria': fields.selection([('1','LABORES'),('2','MATERIALES'),('3','GASTOS'),('4','SUBCONTRATOS'),('5','EQUIPO'),('6','SOBRECOSTOS')],'Categoria',required=False)
                
                }
    #account_invoice_line()