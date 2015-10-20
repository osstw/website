{
    'name': 'Website Portal for Purchases',
    'category': 'Website',
    'summary': (
        'Add your purchase document in the frontend portal (purchases order'
        ', quotations, invoices)'
    ),
    'version': '8.0.1.0.0',
    'author': 'xxxx',
    'website': 'http://www.incaser.es',
    'depends': [
        'purchase',
        'website_portal',
    ],
    'data': [
        'templates/website_portal_purchase.xml',
        'templates/website_portal.xml',
        'templates/website.xml',
    ],
    'demo': [
        # 'data/demo.xml'
    ],
    'installable': True,
}
