var messmenuManagerClass = Class.extend({
    init : function($form, $msgDiv) {
        this.$form = $form;
        this.$msgDiv = $msgDiv;
        this._attachEvents();
    },

    $form : '',
    $msgDiv : '',

    save : function() {
        var $form = this.$form;
        var $msgDiv = this.$msgDiv;
        console.log($form);
        var fields = $form.serializeArray();
        var formArray = {};
        $.each(fields, function(index, field) {
            formArray[field.name] = field.value;
        });
        console.log(formArray);
        var successFunction = function (response) {
            if(response.status == "success") {
                $msgDiv.text('Menu saved');
            }
            else {
                $msgDiv.text('Menu could not be saved');
            }
        };
        bundle = {
            'url' : $form.attr('save_url'),
            'data' : formArray,
            'success' : successFunction,
        };
        ajaxify(bundle, $msgDiv);
    },

    clearMenu : function() {
        this.$form.find('textarea.content').val('');
    },

    resetMenu : function() {
        this.$form.each(function() {
            this.reset();
        });
    },


    _attachEvents : function() {
        var thisObj = this;

        $('[name=save_menu]').click(function() {
            thisObj.save();
        });

        $('[name=clear_menu]').click(function() {
            thisObj.clearMenu();
        });

        $('[name=reset_menu]').click(function() {
            thisObj.resetMenu();
        });

    }

});
