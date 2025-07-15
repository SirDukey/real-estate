# -*- coding: utf-8 -*-
from odoo import api, fields, models


class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'The type of property'
    _order = 'sequence, name'

    # -- Standard fields --
    name = fields.Char(required=True)
    sequence = fields.Integer('Sequence', default=1)

    # -- Relationship fields --
    property_ids = fields.One2many('estate.property', 'property_type_id')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')

    # -- Compute fields --
    offer_count = fields.Integer(compute='_compute_offer_count')

    _sql_constraints = [
        ('check_property_type', 'UNIQUE(name)', 'Property type must be unique.'),
    ]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for row in self:
            if row.offer_ids:
                row.offer_count = len(row.offer_ids)
            else:
                row.offer_count = 0
