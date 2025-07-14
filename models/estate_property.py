# -*- coding: utf-8 -*-
from odoo import api, fields, models, exceptions


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'A table of properties'

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    expected_price_percentage = fields.Integer(default=90)
    selling_price = fields.Float(readonly=False, compute='_compute_selling_price', default=0.0)
    buyer = fields.Char(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string='Garden Area (sqm)')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help='The placement of the garden in relation to the property.'
    )
    is_active = fields.Boolean(active=True, copy=False)
    state = fields.Selection(
        copy=False,
        default='new',
        required=True,
        string='State',
        selection=[
            ('new', 'New'),
            ('offer_received', 'Offer received'),
            ('offer_accepted', 'Offer accepted'),
            ('sold', 'Sold'),
            ('cancelled', 'Cancelled')
        ]
    )

    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    partner_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    user_id = fields.Many2one('res.users', string='Salesman', index=True, tracking=True,
                              default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')

    total_area = fields.Integer(compute='_compute_total_area', string='Total Area (sqm)')
    best_offer = fields.Float(compute='_compute_best_offer')

    _sql_constraints = [
        ('check_property_expected_price', 'CHECK(expected_price >= 0)', 'Expected price cannot be negative.'),
        ('check_property_selling_price', 'CHECK(selling_price >= 0)', 'Selling price cannot be negative.')
    ]

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for row in self:
            if row.garden:
                row.total_area = row.garden_area + row.living_area
            else:
                row.total_area = row.living_area

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for row in self:
            row.best_offer = max(row.offer_ids.mapped('price'), default=0.0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = None
            self.garden_orientation = None

    def action_property_sold(self):
        for row in self:
            if row.state == 'cancelled':
                raise exceptions.UserError('This property is cancelled and cannot be sold.')
            elif row.state in ['new', 'offer_received']:
                raise exceptions.UserError('An offer has not been accepted.')
            elif not row.is_active:
                raise exceptions.UserError('This is property is not active.')
            else:
                row.state = 'sold'
                row.is_active = False
        return True

    def action_property_cancelled(self):
        for row in self:
            if row.state == 'sold':
                raise exceptions.UserError('This property has been sold and cannot be cancelled.')
            else:
                row.state = 'cancelled'
                row.is_active = False
                row.buyer = None
        return True

    @api.depends('offer_ids')
    def _compute_selling_price(self):
        for row in self:
            if row.offer_ids and row.state != 'cancelled':
                for offer in row.offer_ids:
                    if offer.status == 'accepted':
                        row.selling_price = offer.price
                        row.buyer = offer.partner_id.name
                        break
                    else:
                        row.buyer = None
