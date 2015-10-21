# -*- coding: utf-8 -*-
# (c) 2015 Antiun Ingeniería S.L. - Sergio Teruel
# (c) 2015 Antiun Ingeniería S.L. - Carlos Dauden
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.addons.website_sale.controllers.main import website_sale
from openerp.addons.website_sale.controllers.main import QueryURL
from openerp.addons.website.models.website import slug
from openerp import http
from openerp.http import request

from openerp import _


class WebsiteSale(website_sale):

    @http.route(['/supplier/add_product'],
                type='http', auth="user", methods=['POST'], website=True)
    def supplier_add_product(self, name=None, category=0, **post):
        product_obj = request.env['product.product']
        product = product_obj.create(self._prepare_product(name, category))
        return request.redirect("/supplier/product/%s?enable_editor=1" % slug(
            product.product_tmpl_id))

    @http.route(['/supplier/product'],
                type='http', auth="user", methods=['POST'], website=True)
    def supplier_product(self, name=None, category=0, **post):
        product_obj = request.env['product.product']
        product = product_obj.create(self._prepare_product(name, category))
        return request.redirect("/supplier/product/%s?enable_editor=1" % slug(
            product.product_tmpl_id))

    def _prepare_product(self, name=None, category=0):
        vals = {
            'name': name and name or _('New Product'),
            'public_categ_ids': category,
            'manufacturer': request.env.user.partner_id.id
                }
        return vals

    @http.route(['/supplier/product/<model("product.template"):product>',
                 '/supplier/new_product'],
                type='http', auth="public", website=True)
    def supplier_product(self, product=None, category='', search='', **kwargs):
        if product is None:
            product = request.env['product.template']
        values = {
            'search': search,
            'category': category,
            'product': product,
        }
        return request.website.render(
            "website_product_supplier.product", values)

    @http.route(['/supplier/product/save/<model("product.template"):product>',
                 '/supplier/product/save/'],
                type='http', auth="user", website=True)
    def supplier_product_write(self, product=None, **post):
        vals = {
            'name': post.get('name', ''),
            'description_sale': post.get('description_sale', ''),
            'price': post.get('price', 0.0),
            'list_price': post.get('list_price', 0.0),
        }
        if product is None:
            product = request.env['product.template'].create(vals)
        else:
            product.write(vals)

        values = {
            'product': product,
        }
        return request.website.render(
            "website_product_supplier.product", values)
