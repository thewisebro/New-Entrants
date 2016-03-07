


function s()

{
if($('#meerkat-wrap').css('z-index')>0)
return;

$('.search').meerkat({
	
		
		height: '70px',
		width: '100%',
		position: 'bottom',
		close: '.close-meerkat',
		dontShowAgain: '.dont-show',
		animationIn: 'slide',
		animationOut: 'fade',
		animationSpeed: 700
		});
					
					

}


function func1(x)
{

if($.browser.msie && $.browser.version.slice(0,3) =="7.0")
{
$('.ss').css('display','none');
$(x).css('display','block');
alert('1');
if(x=='#my_courses_goto')
s();
}

$('#container').stop().scrollTo(x,800);

w=x;
if($('#go_back').length>0)

$('#container').stop().scrollTo(x,800);

w=x;
if($('#go_back').length>0)
setTimeout('go_back()', 800);
}





