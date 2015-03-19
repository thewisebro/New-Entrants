

$(document).ready(function(){
	//make several slideshows with class selector, all slideshows shares the same parameters
	$('.slideshow').divSlideShow(); 	
	
	//make one slideshow with id selector
	$('#dss,#plug-and-play').divSlideShow({
		height:200, 
		width:960, 
		arrow:"split",
		loop:3,
		slideContainerClass:"slide-container",
		separatorClass:"separator", 
		controlClass:"control",  
		leftArrowClass:"control", 
		rightArrowClass:"control", 
		controlActiveClass:"control-active",
		controlHoverClass:"control-hover",
		controlContainerClass:"control-container"
		
	});
	
	
	
});

function manipulate()
{
	$.divSlideShow.slideTo('#plug-and-play',$('#test_gotoPage').val()-1);
}




//tabbed slideshow

		jQuery(document).ready(function($){
			$('.tabs').each(function(){
				$(this).find('li:first').addClass('current'); // set the first tab to display
				repeat_slideshow($(this));
			});
			$('.tabs li .tab-select').click(function(){
				$(this).closest('.tabs').find('li').not($(this).parent()).removeClass('current'); // hide all tabs except for the current
				$(this).parent().addClass('current'); // set the current tab to display
				reset_slideshow($(this).closest('.tabs'));
				return false;
			});
			function slideshow(slide)
			{
				var index = slide.find('li.current').index();
				var total = slide.find('li').length;
				if ( index+1 >= total )
					var next = 0;
				else
					var next = index + 1;
				slide.find('li.current').removeClass('current');
				slide.find('li').eq(next).addClass('current');
			}
			function repeat_slideshow(slide)
			{
				slide.data('slideshow', setTimeout(function(){
						slideshow(slide);
						repeat_slideshow(slide);
					}, 5000));
			}
			function stop_slideshow(slide)
			{
				clearTimeout(slide.data('slideshow'));
			}
			function reset_slideshow(slide)
			{
				stop_slideshow(slide);
				repeat_slideshow(slide);
			}
		});




	$(function () {

			var H1=$("div.quote_container").css('height');
			var H2=$("div.quote").css('height');
			var H3=$("div.downstrip").css('height');
			var H4=$("header.main-header").css('height');
			$(".quote").css('margin-top', ((parseInt(H1,10)-parseInt(H2,10)-parseInt(H3,10)-parseInt(H4,10))/2 + 'px'));
		
	});

	$(window).resize(function(){
			var H1=$("div.quote_container").css('height');
			var H2=$("div.quote").css('height');
			var H3=$("div.downstrip").css('height');
			var H4=$("header.main-header").css('height');
			$(".quote").css('margin-top', ((parseInt(H1,10)-parseInt(H2,10)-parseInt(H3,10)-parseInt(H4,10))/2 + 'px'));
		});




$(document).ready(function(){
	$('a[href^="#"]').on('click',function (e) {
	    e.preventDefault();

	    var target = this.hash,
	    $target = $(target);

	    $('html, body').stop().animate({
	        'scrollTop': $target.offset().top
	    }, 400, 'swing', function () {
	        window.location.hash = target;
	    });
	});
});


// $(function () {
// 	$('img.open-close_image').click(function(){
// 		var $this= $(this);
// 		if ($this.attr('class')=='open-close_image rotated') {
// 			$this.removeClass("rotated");
// 		} else{
// 			$this.addClass("rotated");
// 		};
//    	});
// });

$(function () {
	var degrees=45;
	$('img.open-close_image').on('click', function () {
		degrees=degrees+45;
		$(this).css({
			'transform': 'rotate(' + degrees + 'deg)',
			'-webkit-transform': 'rotate(' + degrees + 'deg)',
			'-moz-transform': 'rotate(' + degrees + 'deg)',
			'-ms-transform': 'rotate(' + degrees + 'deg)',
			'transition-duration': 0.4+'s',
			'transition-property':'transform'
		}, 400);
	});
	

});

//blog archives

$(function () {
	$('span.current_year_container').on('click', function () {
		$('ul.year_list').slideToggle(200);

	});

	$('ul.year_list li').on('click', function () {
		$('span.current_year').text($(this).text());
		$('ul.year_list').slideUp(100);
		var disp=$(this).attr('id');
		var divdisp=$('div#'+disp);
		divdisp.slideDown(400);
		divdisp.siblings().slideUp(200);
	});
});


$(document).ready(function(){

			$('li.expand').click(function(){
				$(this).children('.content').slideToggle(400);
				console.log('twas clicked');
			});			
		});

//fade effect of quotes
$(function () {
	$('div.fadediv').hide()
		 	.fadeIn(400);
});