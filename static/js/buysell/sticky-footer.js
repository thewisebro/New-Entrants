$(document).ready(function() {
	var docHeight = $(window).height();
	var footerHeight = $('#footer').height();
	var footerTop = $('#footer').position().top + footerHeight;
	if (footerTop < docHeight) {
	$('#footer').css('margin-top',(docHeight - footerTop) + 'px');
	}
	 if (footerTop > docHeight)
    {
	  $('#footer').css({'position': 'relative'}).css({'margin-top':'50px'});
    }
	});
