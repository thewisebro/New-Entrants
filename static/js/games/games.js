$(document).ready(function(){ 
  
  if(typeof(Storage)!=="undefined")
  {
    if(typeof(sessionStorage.p)!=="undefined")
    {
      if(sessionStorage.p==1)
      {
        $(".bottom-slider").css({'display':'block'});
        $("#footer").css({'display':'none'});
      }
      else if(sessionStorage.p==0)
      {
        $(".bottom-slider").css({'display':'none'});
        $("#footer").css({'display':'block'});  
      }
    }
    else
    {
      sessionStorage.p=0;
    }
  }
   $(".games_links").click(function(){
     $('.nano').nanoScroller();  
     var display = $("#scroll_slider").css("display")
     if(display == 'none')
     {  
      $(".bottom-slider").css({'display':'block'});
      $("#footer").css({'display':'none'}); 
       if(typeof(Storage)!=="undefined")
       {
         sessionStorage.p=1;
       }
     }
     else
     {
        $(".bottom-slider").css({'display':'none'}); 
        $("#footer").css({'display':'block'}); 
         if(typeof(Storage)!=="undefined")
         {
           sessionStorage.p=0;
         }
     } 
  });
});

