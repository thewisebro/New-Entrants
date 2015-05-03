var commentManagerClass = Class.extend({
	init : function(commentEditor, commentLister) {
		this.commentEditor = commentEditor;
		this.commentLister = commentLister;

		this._attachEvents();
	},

	commentEditor : '',
	commentLister : '',


	save : function(formArray) {
		$errorMsgDiv = this.commentEditor.$dom.find('.error_msg');
		$errorMsgDiv.text('');
		// call api for saving to DB
		var thisObj = this;
		var successFunction = function (response) {
			if(response.status == 'success') {
				thisObj.commentLister.save(formArray, response.data['id']);
				thisObj.commentEditor.$dom.trigger('to_commentEditor_data_saved');
			}
			else {
				$errorMsgDiv.text(response.error_msg);
			}
		};
		bundle = {
			'url' : this.commentEditor.$dom.attr('add_comment_url'),
			'data' : formArray,
			'success' : successFunction
		};
		ajaxify(bundle, this.commentEditor.$dom.find('.error_msg'));
	},

	delete : function(comment_id) {
		// call api for deleting from DB
		formArray = {};
		formArray['id'] = comment_id;
		var thisObj = this;
		var successFunction = function (response) {
			if(response.status == 'success') {
				thisObj.commentLister.delete(response.data['id']);
			}
		};
		bundle = {
			'url' : this.commentEditor.$dom.attr('delete_comment_url'),
			'data' : formArray,
			'success' : successFunction
		};
		ajaxify(bundle);
	},

	_attachEvents : function() {
		var thisObj = this;

		this.commentEditor.$dom.bind('from_commentEditor_save', function(event, formArray){
			thisObj.save(formArray);
		});

		this.commentLister.$dom.bind('from_commentLister_delete', function(event, comment_id){
			thisObj.delete(comment_id);
		});

	}
});
