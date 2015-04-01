var mainClass = Class.extend({
    init : function() {
        this._attachEvents();
    },

    selectFromDropDown : function($option) {
        window.location.href = $option.val();
    },

    _attachEvents : function() {
        var thisObj = this;

        $('select.dropdown').change(function() {
            thisObj.selectFromDropDown($(this));
        });
    }

});

$(document).ready(function() {
    var main = new mainClass();
});
