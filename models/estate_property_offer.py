# -*- coding: utf-8 -*-
import pdb

from odoo import api, fields, models, exceptions
from odoo.tools import date_utils


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Offer made on a property'
    _order = 'price desc'

    # -- Standard fields --
    price = fields.Float()
    validity = fields.Integer(default=7)
    status = fields.Selection(
        copy=False,
        string='Status',
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ]
    )

    # -- Relationship fields --
    # TODO: I first tried fields.Char but got a field type mismatch, used Many2one in place. Research this further...
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)
    partner_id = fields.Many2one('res.partner', string='Buyer', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)

    # -- Compute fields --
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline', store=True)

    _sql_constraints = [
        ('check_property_offer_price', 'CHECK(price >= 0)', 'Offer price cannot be negative.'),
    ]

    @api.depends('validity')
    def _compute_date_deadline(self):
        for row in self:
            if row.create_date:
                row.date_deadline = date_utils.add(fields.Date.to_date(row.create_date), days=row.validity)
            else:
                row.date_deadline = date_utils.add(fields.Date.today(), days=row.validity)

    def _inverse_date_deadline(self):
        for row in self:
            if row.date_deadline:
                row.validity = (row.date_deadline - fields.Date.to_date(row.create_date)).days
            else:
                row.validity = 7

    def action_property_offer_accept(self):
        for row in self:
            minimum_expected_selling_price = row.property_id.expected_price * row.property_id.expected_price_percentage / 100
            if not row.property_id.is_active:
                raise exceptions.UserError('The property is not active, the offer cannot be changed')
            elif row.property_id.state == 'offer_accepted':
                raise exceptions.UserError('An offer has already been accepted')
            elif row.property_id.state == 'sold':
                raise exceptions.UserError('The property has been sold, the offer cannot be changed')
            elif row.price < minimum_expected_selling_price:
                raise exceptions.ValidationError(f'The offer is below the minimum expected price of {minimum_expected_selling_price}.')
            else:
                row.status = 'accepted'
                row.property_id.state = 'offer_accepted'
        return True

    def action_property_offer_refuse(self):
        for row in self:
            if row.property_id.is_active and row.property_id.state != 'sold':
                row.status = 'refused'
                row.property_id.state = 'offer_received'
            elif row.property_id.state == 'sold':
                raise exceptions.UserError('The property has been sold, the offer cannot be changed')
            else:
                raise exceptions.UserError('The property is not active, the offer cannot be changed')
        return True

    @api.model
    def create(self, vals):
        property_id = self.env['estate.property'].browse(vals['property_id'])
        highest_offer = max([offer_id.price for offer_id in property_id.offer_ids], default=0.0)
        if vals['price'] < highest_offer:
            raise exceptions.ValidationError(f'There is a higher offer of {highest_offer}')
        property_id.state = 'offer_received'
        return super().create(vals)
