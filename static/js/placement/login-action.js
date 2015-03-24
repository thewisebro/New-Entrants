current='login';
function alertmsg(){ alert("Mayank");}



function changeText(changeto){
	document.getElementById('box_'+current).style.display='none';
	document.getElementById('box_'+changeto).style.display='block';
	
	$("#login_box_top_links_"+current).removeClass("login_box_top_link_selected");
	$("#login_box_top_links_"+changeto).addClass("login_box_top_link_selected");
	current=changeto;
}

function descriptionSlideUp(){
	$('#public_box_text').animate({
		'margin-top': '331px'
	},400,function(){});
}


function descriptionSlideDown(){
	$('#public_box_text').animate({
		'margin-top': '411px'
	},400,function(){});
}

$(document).ready(function(){
	$('#public_box').mouseover(function() {
		descriptionSlideUp();
	});
	
	$('#top_right_dropdown').click(function() {
		$('#top_right_dropdown_menu').toggle();
	});

	$('#public_box').mouseleave(function() {
		setTimeout('descriptionSlideDown()',2000);
	});
});

