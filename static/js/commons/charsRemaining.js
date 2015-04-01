var charsRemainingClass = Class.extend({
	init : function(containerXPath) {
		this.elementXPath = containerXPath + ' textarea[max-length]';
		this.containerXPath = containerXPath;
		this._attachEvents();
	},

	elementXPath : '',

	limitChars : function($element, keyCode) {
		var max_chars = $element.attr('max-length');
		var charsRemaining = max_chars - $element.val().length;
		if(charsRemaining <= 0)
		{
			if((keyCode >= 48 && keyCode <= 90) || 
				(keyCode >= 96 && keyCode <= 111) || 
				(keyCode >= 186 && keyCode <= 192) || 
				(keyCode >= 219 && keyCode <= 222) ||
				(keyCode >= 13 && keyCode <= 32))
			{
				return false;
			}
		}
	},

	displayChars : function($element) {
		var max_chars = $element.attr('max-length');
		var charsRemaining = max_chars - $element.val().length;
		if(charsRemaining <= 0)
		{
			$element.val($element.val().substr(0, max_chars));
			charsRemaining = 0;
		}
		$element.closest(this.containerXPath).find('.chars_remaining').text(charsRemaining);
	},

	_attachEvents : function() {
		var that = this;

		$(document).on('keydown', this.elementXPath, function(event) {			
			var limit = that.limitChars($(this), event.keyCode);
			return limit;
		});

		$(document).on('keyup', this.elementXPath, function(event) {			
			that.displayChars($(this));
		});
	}

});
