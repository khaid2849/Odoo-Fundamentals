# -*- coding: utf-8 -*-
{
    "name": "Ondoo - Theme",
    "summary": """
    """,
    "description": """
    """,
    "author": "Ondoo JSC",
    "website": "",
    "category": "",
    "version": "15.0.0.1",
    "depends": ["web", "base"],
    "data": [],
    "installable": True,
    "assets": {
        "web.assets_backend": [
            "/ondoo_theme/static/src/css/base.css",
            "/ondoo_theme/static/src/css/form_asset.css",
            "/ondoo_theme/static/src/scss/base_enterprise.scss",
            "/ondoo_theme/static/src/js/ondoo_user_menu.js",
            "/ondoo_theme/static/src/js/ondoo_required_fields_label.js",
            # "/ondoo_theme/static/src/xml/view_base.xml",
        ],
        # 'web.assets_qweb': [
        #     'account/static/src/xml/**/*',
        # ],
        "web.assets_frontend": [
            "ondoo_theme/static/src/css/front_end.css",
        ],
    },
    "images": ["static/description/icon.png"],
}
