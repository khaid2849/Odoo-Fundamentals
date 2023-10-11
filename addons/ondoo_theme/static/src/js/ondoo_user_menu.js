/** @odoo-module **/

import {UserMenu} from "@web/webclient/user_menu/user_menu";

import {patch} from 'web.utils';

patch(UserMenu.prototype, 'ondoo_theme/static/src/js/ondoo_user_menu.js', {
    /**
     * @override
     */
    getElements() {
        var sortedItems = this._super(...arguments);
        sortedItems = sortedItems.filter(item => item.id == 'shortcuts' || item.id == 'settings' || item.id == 'logout')
        return [sortedItems[1], sortedItems[0], sortedItems[2]]
    }

})