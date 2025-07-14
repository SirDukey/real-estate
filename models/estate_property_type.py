# -*- coding: utf-8 -*-
from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'The type of property'

    name = fields.Char(required=True)

    _sql_constraints = [
        ('check_property_type', 'UNIQUE(name)', 'Property type must be unique.'),
    ]
