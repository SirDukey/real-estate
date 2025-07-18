# -*- coding: utf-8 -*-
from odoo import api, exceptions, fields, models


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'A table of properties'
    _order = 'id desc'

    # -- Standard fields --
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    expected_price_percentage = fields.Integer(default=90)
    buyer = fields.Char(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string='Garden Area (sqm)')
    is_active = fields.Boolean(active=True, copy=False)
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help='The placement of the garden in relation to the property.'
    )
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

    # -- Relationship fields --
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    partner_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    salesperson_id = fields.Many2one('res.users', string='Salesperson', index=True, tracking=True,
                                     default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tags')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')

    # -- Compute fields --
    selling_price = fields.Float(readonly=False, compute='_compute_selling_price', default=0.0)
    total_area = fields.Integer(compute='_compute_total_area', string='Total Area (sqm)')
    best_offer = fields.Float(compute='_compute_best_offer')

    # -- Constraints --
    _sql_constraints = [
        ('check_property_expected_price', 'CHECK(expected_price >= 0)', 'Expected price cannot be negative.'),
    ]

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price < 0.0:
                raise exceptions.ValidationError("Selling price cannot be negative")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            if record.garden:
                record.total_area = record.garden_area + record.living_area
            else:
                record.total_area = record.living_area

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped('price'), default=0.0)

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = None
            self.garden_orientation = None

    def action_property_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise exceptions.UserError('This property is cancelled and cannot be sold.')
            elif record.state in ['new', 'offer_received']:
                raise exceptions.UserError('An offer has not been accepted.')
            elif not record.is_active:
                raise exceptions.UserError('This is property is not active.')
            else:
                record.state = 'sold'
                record.is_active = False
        return True

    def action_property_cancelled(self):
        for record in self:
            if record.state == 'sold':
                raise exceptions.UserError('This property has been sold and cannot be cancelled.')
            else:
                record.state = 'cancelled'
                record.is_active = False
                record.buyer = None
        return True

    @api.depends('offer_ids')
    def _compute_selling_price(self):
        for record in self:
            if record.offer_ids and record.state != 'cancelled':
                for offer in record.offer_ids:
                    if offer.status == 'accepted':
                        record.selling_price = offer.price
                        record.buyer = offer.partner_id.name
                        break
                    else:
                        record.buyer = None

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_cancelled(self):
        if any(record.state not in ['new', 'cancelled'] for record in self):
            raise exceptions.UserError("Only 'New' or 'Cancelled' properties may be deleted.")
