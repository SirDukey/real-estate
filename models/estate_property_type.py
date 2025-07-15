# -*- coding: utf-8 -*-
from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'The type of property'
    _order = 'sequence, name'

    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1)

    property_ids = fields.One2many('estate.property', 'property_type_id')

    _sql_constraints = [
        ('check_property_type', 'UNIQUE(name)', 'Property type must be unique.'),
    ]
