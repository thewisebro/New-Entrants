

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


//team page: On clicking the tab, the ID of the tab is taken as variable, say if "II" is selected, and its ID = "II", that's taken in the variable disp, and the class of the required divs to be displayed are kept same as the ID of the selected tab. So in this case, divs having "II" as class will be displayed.

$(function () {
	$('span.team-tab').on('click', function () {
    $("#lightbox").remove(); //for lightbox to work properly: The lightbox works by first creatingall the lightbox divs when any of the team member is clicked upon(see team2.htm inline javascript), and then hiding all other lightbox divs other than the one to be displayed, then on clicking upon any navigation button, it moves across the lightboxes using indices. So the lightbox div is created only once, when any of the lightbox triggers is clicked for the first time. So if suppose all the 40 team members are being displayed, and one of the lightboxtriggers is clicked, all the 40 lightbox divs get created. Now if a tab "III" is clicked, that won't make any difference in the lightbox. it will still move across the 40 team members. so for that, each time the tab is clicked we remove the lightbox div, so that it can only move across the required team members.
		$(this).addClass('active'); // for styling the selected tab
		$(this).siblings().removeClass('active');
		var disp=$(this).attr('id');
		var divdisp=$('div.'+disp);
    //fadOut all the divs (then fadeIn the div in the next section which is required to be displayed)
		$('span.team-tab').each(function(){
			var curr=$(this).attr('id');
			$('div.'+curr).fadeOut(0);
      $('div.'+curr+'> a').removeClass("lightboxTrigger");
		});
    //fadeIn the required div
		divdisp.fadeIn(200);
    $('div.'+disp+'> a').addClass("lightboxTrigger");

	});

	$('span#all').on('click', function () {
    $("#lightbox").remove(); //for lightbox to work properly
		$('span.team-tab').each(function(){
			var curr=$(this).attr('id');
			$('div.'+curr).fadeIn(200);
      $('div.'+curr+'> a').addClass("lightboxTrigger");
		});
	});

	$('span.team-tab2').on('click', function () {
		$(this).addClass('active');
		$(this).siblings().removeClass('active');
		var disp=$(this).attr('id');
		var divdisp=$('div.'+disp);
		$('span.team-tab2').each(function(){
			console.log($(this).text());
			var curr=$(this).attr('id');
			$('div.'+curr).fadeOut(200);
		});

		divdisp.fadeIn(400);
	});

	$('span#all').on('click', function () {
		$('span.team-tab2').each(function(){
			var curr=$(this).attr('id');
			$('div.'+curr).fadeIn(200);
		});
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

//hide arrows in index.htm when blog posts less than 3
$(document).ready(function(){
		var ln=$('.box').length;
		if(ln<4){
		$('.control').hide()
		$('.dssSlideContainer').css("margin-left","-50px");
		}
		});


//contact 

$(document).ready(function(){
	$('.success_message').fadeIn('slow').delay(5000).hide(0);
});