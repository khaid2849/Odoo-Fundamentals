/** @odoo-module **/

import { FormLabel } from "@web/views/form/form_label";
import {patch} from 'web.utils';
import { fieldVisualFeedback } from "@web/views/fields/field";

patch(FormLabel.prototype, 'ondoo_theme/static/src/js/ondoo_required_fields_label.js', {
    /**
     * @override
     */
    get className() {
        var class_name = this._super(...arguments);
        const classes = [class_name];
        const { readonly, required, invalid, empty } = fieldVisualFeedback(
            this.props.fieldInfo.FieldComponent,
            this.props.record,
            this.props.fieldName,
            this.props.fieldInfo
        );
        if(required){
            classes.push('ondoo_required_label');
        }
        return classes.join(" ");
    }
})