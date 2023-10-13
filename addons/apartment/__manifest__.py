# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    "name": "Industrial Area Management",
    "version": "0.1",
    "author": "khaid",
    "category": "Administration",
    "depends": ["base", "ondoo_theme", "account"],
    "description": """
Quản lý khu công nghiệp: 
====================
Quản lý và tổ chức thực hiện chức năng cung ứng dịch vụ hành chính công và địch vụ hỗ trợ khác có liên quan đến hoạt động đầu tư và sản xuất kinh doanh cho nhà đầu tư trong khu công nghiệp. 
""",
    "data": [
        "security/ir.model.access.csv",
        "views/menu.xml",
        "views/nha_cung_cap.xml",
        "views/chu_dau_tu.xml",
        "views/khach_hang.xml",
        "views/thiet_bi_tai_san.xml",
        "views/dich_vu.xml",
        "views/nganh_nghe.xml",
        "views/so_do_kcn.xml",
        "views/su_kien.xml",
        "views/tin_tuc.xml",
        "views/quoc_gia.xml",
    ],
    "license": "LGPL-3",
}
