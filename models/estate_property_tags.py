# -*- coding: utf-8 -*-
from odoo import api, fields, models


class EstatePropertyTags(models.Model):
    _name = 'estate.property.tags'
    _description = 'A tag which can be added to a property'

    name = fields.Char(required=True)

    _sql_constraints = [
        ('check_property_tags', 'UNIQUE(name)', 'Property tag must be unique.'),
    ]
