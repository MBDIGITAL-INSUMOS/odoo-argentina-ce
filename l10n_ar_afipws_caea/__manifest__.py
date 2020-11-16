{
    'name': "Factura Electrónica Argentina CAEA",

    'summary': """
        Habilit< la gestion de CAEA""",
    'sequence': 14,

    'description': """
         Permita consignar en los comprobantes respaldatorios de las operaciones,
          el Código de Autorización Electrónico Anticipado "CAEA", en reemplazo del "CAE"     """,
    'author': "Filoquin",
    'website': "http://www.sipecu.com.ar",

    'category': 'Localization/Argentina',
    'version': '13.0.1.0.0',
    'depends': ['l10n_ar_afipws_fe'],

    'data': [
        'security/ir.model.access.csv',
        'views/afipws_caea.xml',
        'views/company.xml',
        'views/res_config_settings.xml',
    ],
    'demo': [
        #'demo/demo.xml',
    ],
}
