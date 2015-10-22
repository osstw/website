# -*- coding: utf-8 -*-
# (c) 2015 Antiun Ingeniería S.L. - Sergio Teruel
# (c) 2015 Antiun Ingeniería S.L. - Carlos Dauden
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import http
from openerp.http import request


class WebsiteProductSupplier(http.Controller):

    mandatory_product_fields = ['name']
    optional_product_fields = ['description', 'list_price']

    def _get_mandatory_product_fields(self):
        return self.mandatory_product_fields

    def _get_optional_product_fields(self):
        return self.optional_product_fields

    def check_product_form_validate(self, data):
        error = dict()
        for field_name in self._get_mandatory_product_fields():
            if not data.get(field_name):
                error[field_name] = 'missing'
        return error

    def _post_prepare_product_query(self, product_dic, data):
        return product_dic

    def product_field_parse(self, data):
        # set mandatory and optional fields
        all_fields = self._get_mandatory_product_fields() + \
                     self._get_optional_product_fields()
        # set data
        if isinstance(data, dict):
            product_dic = dict((field_name, data[field_name])
                         for field_name in all_fields if field_name in data)
        else:
            product_dic = dict((field_name, getattr(data, field_name))
                         for field_name in all_fields)
        product_dic = self._post_prepare_product_query(product_dic, data)
        return product_dic

    def product_values(self, post):
        values = {
            'product': self._prepare_supplier_product(post),
        }
        return values

    @http.route(['/supplier/product/<model("product.template"):product>',
                 '/supplier/new_product'],
                type='http', auth="user", website=True)
    def supplier_product(self, product=None, category='', search='', **post):
        values = {
            'search': search,
            'category': category,
            'main_obj': product,
            'error': {},
        }
        if product is None:
            product = request.env['product.template']
            values['main_obj'] = product
        values['product'] = self.product_field_parse(product)
        return request.website.render(
            "website_product_supplier.product", values)


    @http.route(['/supplier/product/save/<model("product.template"):product>',
                 '/supplier/product/save/'],
                type='http', auth="user", website=True)
    def supplier_product_save(self, product=None, **post):
        product_tmp_obj = request.env['product.template']
        values = {
            'main_obj': product,
            'product': self.product_field_parse(post),
        }
        values["error"] = self.check_product_form_validate(values["product"])
        if values["error"]:
            if product is None:
                values['main_obj'] = product_tmp_obj
            return request.website.render(
                "website_product_supplier.product", values)

        if product is None:
            vals = values['product']
            vals.update(manufacturer=request.env.user.partner_id.id)
            values['main_obj'] = product_tmp_obj.sudo().create(vals)
        else:
            product.write(values['product'])

        return request.website.render(
            "website_product_supplier.product", values)



    @http.route(['/supplier/product/list'],
                type='http', auth="user", website=True)
    def supplier_product_list(self, **post):
        product_tmp_obj = request.env['product.template']
        domain = [('manufacturer', '=', request.env.user.partner_id.id)]
        products = product_tmp_obj.search(domain)
        values = {
            'products': products,
        }

        return request.website.render(
            "website_product_supplier.product_list", values)
