odoo.define("your_module_name.custom_buttons", function (require) {
  "use strict";

  var core = require("web.core");
  var FormController = require("web.FormController");

  FormController.include({
    renderButtons: function ($node) {
      this._super.apply(this, arguments);

      if (this.$buttons) {
        this.$buttons
          .find(".o_form_button_create span")
          .text("New Label for Create"); // Change 'New Label for Create' to your desired label for Create button
        this.$buttons
          .find(".o_form_button_edit span")
          .text("New Label for Edit"); // Change 'New Label for Edit' to your desired label for Edit button
        // You can change other button labels similarly if needed
      }
    },
  });
});
