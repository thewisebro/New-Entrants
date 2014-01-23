
/*for loading the diff links in mainbody div*/
  function lTrending(){


 //        $('#centerdata').load('./links/trending.html #trending_div');    

           $('#centerdata').css('width',$(window).width()-180);
    
          resizeit('container','item_wrapper','item');

        }


    function lAlbums(){
//        $('#centerdata').load('./links/artists.html #albumsList');
      $("#centerdata").css('width',$(window).width()-180-240);

        setTimeout(function() { // nano scroll bar start
              $(".nano").nanoScroller({ preventPageScrolling: true });
              $('#oneAlbumOpened').animate({left:'220',right:'0'},300);
              $('#album_panel_hide').animate({left:'420',top:'185'},300);
              $("#rightside").animate({right:'0'},300); 
            },10);  
    }

   
    function lArtists(){
          $("#centerdata").css('width',$(window).width()-180-240);

//        $('#centerdata').load('./links/artistslist.html #artistsList');
         setTimeout(function() {
           // nano scroll bar start
      	      $(".nano").nanoScroller({ preventPageScrolling: true });
              $("#artist_view").animate({left:'220', right:'0'},300);
              $("#artist_panel_hide").animate({left:'420', top:'145'},300);
              $("#rightside").animate({right:'0'},300);
},10);
    
    }

        function lStumble(){
        $('#centerdata').load('./links/searchView.html #oneAlbumOpened');
        setTimeout(function() { // nano scroll bar start
            


        },20);  
      }




// setting the width of center div on load 

$( document ).ready(function() {
    // $('#centerdata').css('width',$(window).width()-180-280);
     
     // fix for placeholder in chrome
      $('input:text, textarea').each(function(){
          var $this = $(this);
          $this.data('placeholder', $this.attr('placeholder'))
               .focus(function(){$this.removeAttr('placeholder');})
               .blur(function(){$this.attr('placeholder', $this.data('placeholder'));});
      });


});

// setting the width of center div on resize
$(window).resize(function() {
       $('#centerdata').css('width',$(window).width()-180-240);

       //var selectedTab = $('#navigation a.selected');
       //if($('#navigation a.selected') == $('#trending_link')){alert('ad');}
       //else{alert('else');}
});

// bind search with keydown 
$(document).bind('keydown',function(e){

    $('#searchinput').focus();
    // $(document).unbind('keydown');
    // var duck=10;
});


// search 
function searchView(e){
  if($(e).hasClass("notOpen")){
    // search icon css
    $(e).removeClass("notOpen");
    // alert(' open/visible ');
    // change the style of search div
    $("#searchDivcss").removeClass("searchLightboxClose").addClass("searchLightboxOpen");
  }
  else{
    // search icon css
    // alert("not visible");
    $(e).addClass("notOpen");
    // active class on full search view only
    // change the style of search div
    $("#searchDivcss").removeClass("searchLightboxOpen").addClass("searchLightboxClose");
  }
}
