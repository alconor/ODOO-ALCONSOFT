# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################


{
    'name': 'Anexos Fiscales de DGI Panamá',
    'version': '1.1',
    'category': 'Hidden/Dependency',
    'description': """
Anexos Fiscales de DGI Panamá
Anexos 72, 79 y 94 de Software "Renta 2014"
Formulario 43 de Software "Informes de Contribuyente"
versión 2015-06-19 20:26

""",
    'author': 'Alconsoft-Sistech',
    'website': 'http://alconsoft.net',
    'depends': ['account','fleet'],
    'init_xml':[],
    'data': ['anexos_view_p.xml'],
    'demo': [],
    'installable': True,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
