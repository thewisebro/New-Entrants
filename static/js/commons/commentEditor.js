var commentEditorClass = Class.extend({
	init : function(domXPath, $charsRemaining, formHtml) {
		this.domXPath = domXPath;
		if(formHtml == null)
			this.formHtml = this.defaultFormHtml;
		else
			this.formHtml = formHtml
		$(domXPath).html(this.formHTML);
		this.$form = $(domXPath).children('form[name=comment_edit]');
		this.$form.find('.chars_remaining').text(this.$form.find('[name=comment]').attr('max-length'));
		this.$dom = $(this.domXPath);
		this._attachEvents($charsRemaining);
	},

	domXPath : '',
	formHtml : '',
	$form : '',
	$dom : '',

	clearForm : function() {
		this.$form.find('input:text, input:password, input:file, select, textarea').val('');
		this.$form.find('textarea').focus();
	}

	save : function() {
		var validate = true;
		/** form validation **/
		if($(this).val() == '')
		{
			validate = false;
			$(this).addClass('error');
		}
		// validate required name, field1, message; field2 <-> field_join2

		if(validate)
		{	// if form is validated
			var fields = this.$form.serializeArray();
			var formArray = {};
			$.each(fields, function(index, field) {
				formArray[field.name] = field.value;
			});
			this.$form.trigger('from_commentEditor_save', formArray);
		}
	},

	_attachEvents : function($charsRemaining) {
		var that = this;

		$(document).on('submit', this.domXPath + ' form[name=comment_edit]', function(e) {
			that.save();
			if($charsRemaining != null)
				$charsRemaining.displayChars($(that.domXPath + ' form[name=comment_edit] [name=comment]'))
			e.preventDefault();
		});

	},


	defaultFormHtml : '\
	<form name="comment_edit" action="">\
		<div class="textarea_container">\
			<textarea name="comment" max-length="100"></textarea>\
			<div class="footer">\
				<span class="right_float">
					<font class="chars_remaining">100</font> chars remaining
				</span>\
			</div>\
		</div>\
		<input type="submit" value="Post" class="button" />\
		<div class="error_msg"></div>\
	</form>'

});
