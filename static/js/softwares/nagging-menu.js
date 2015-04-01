$(function() 
{ 
// grab the initial top offset of the navigation 
  var sticky_navigation_offset_top = $('#menu').offset().top;
// our function that decides weather the navigation bar should have "fixed" css position or not.
  var sticky_navigation = function()
  {
    var scroll_top = $(window).scrollTop(); 
// our current vertical position from the top      
// if we've scrolled more than the navigation, change its position to fixed to stick to top,
// otherwise change it back to relative
    if (scroll_top > sticky_navigation_offset_top)
    { 
      $('#menu').css({ 'position': 'fixed', 'top':0, 'left':0,'width':'100%','z-index':10 });
		  $('#w ul').css("margin","75px 0px 0px 12px");
		  $('#l ul').css("margin","75px 0px 0px 12px");
    }
    else
    {
      $('#menu').css({'position': 'relative'});
		  $('#w ul').css("margin","80px 0px 0px 4px");
		  $('#l ul').css("margin","-252px 0px 0px 4px");
		  $('#sc1').css({'margin-top':'10px'});   
    }   
  };    
// run our function on load
  sticky_navigation();
// and run it again every time you scroll
  $(window).scroll(function()
  {
    sticky_navigation();
  });
});
