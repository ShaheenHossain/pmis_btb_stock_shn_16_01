odoo.define('btb_stock.odoo_tutorial', function (require) {
    'use strict';

    console.log('popup.js loaded');
    var FormController = require('web.FormController');

    var ExtendFormController = FormController.include({
        saveRecord: function () {
             console.log('saveRecord');
            var res = this._super.apply(this, arguments);
            this.do_notify("Success","Record Saved");
            return res;
            }
        });
       });