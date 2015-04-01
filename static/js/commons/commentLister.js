var commentListerClass = Class.extend({
	init : function(domXPath) {
		this.$dom = $(domXPath);
		this.domXPath = domXPath;

		this._attachEvents();
	},

	domXPath : '',
	$dom : '',

	save : function(formArray, id) {
		var $dom = this.$dom;
		var $comment = $dom.find('.comment');
		if($comment.length == 0)
			$comment = $dom.prepend(this.commentHtml).find('.comment:eq(0)');
		$.each(formArray, function(name, value) {
			$comment.find('[name=' + name + ']').text(value);
		});
		$comment.attr('id', id);		
	},

	callDelete : function($deleteButton) {
		var $comment = $deleteButton.closest('.comment');
		var commentId = $comment.attr('id')
		$deleteButton.trigger('from_commentLister_delete', commentId);
	},

	delete : function(commentId) {
		var $comment = this.$dom.find('.comment#' + commentId);
		$comment.remove();
	},

	_attachEvents : function() {
		var that = this;

		$(document).on('click', this.domXPath + ' .delete', function(){
			that.callDelete($(this));
		});
	},

	commentHtml : '\
	<li class="comment">\
		<div class="pic">\
			<img src="" />\
		</div>\
		<div class="left">\
			<div class="top">\
				<span class="name left_float"></span>\
				<span class="time right_float"></span>\
			</div>\
			<div class="text">\
			<div>\
		</div>\
		<div class="right">\
			<span class="close_cross delete">X</span>\
		</div>\
	</li>\
	'
});
