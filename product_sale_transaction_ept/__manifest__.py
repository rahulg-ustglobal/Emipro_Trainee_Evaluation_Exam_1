{
    'name':'Product Sale Transaction',
    'author':'rahulg-ept',
    'version':'1.0',
    'summary':'Product Sale Transaction',
    'description': """Product Sale Transaction""",
    'depends' : ['base'],
    'data':[
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'wizard/view_sale_order.xml',
        'views/view_product_uom.xml',
        'views/view_product.xml',
        'views/view_res_partner.xml',
        'views/view_field_visit.xml',
        'views/view_sale_order.xml'

    ],
    'demo':[],
    'installable':True,
    'auto_install': False,
    'application':False
}
