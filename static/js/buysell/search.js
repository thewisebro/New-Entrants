$(document).ready(function(){
	$('#search-btn').click(function(){
		var type = $('#search-select select').val();
		var name = $('#search-input').val();
		if(type != '' && name!='') document.location.href = '/buysell/search/' + type + '/' + name + '/';
		else alert("Please fill in the details first");
	});
});
