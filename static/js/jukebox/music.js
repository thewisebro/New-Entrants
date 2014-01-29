
/*for loading the diff links in mainbody div*/
  function lTrending(){
         //  $("#rightside").animate({right:'220',opacity:'0'},300); 
          resizeit('container','item_wrapper','item');

        }


    function lAlbums(){

        setTimeout(function() {
              $(".nano").nanoScroller({ preventPageScrolling: true });
              listopen='true';
              $('#oneAlbumOpened').animate({left:'220',right:'0'},300);
              $('#album_panel_hide').animate({left:'420',top:'185'},300);
             // $("#rightside").animate({right:'0',opacity:'1'},300); 
            },10);  
    }

   
    function lArtists(){

        setTimeout(function() {
      	      $(".nano").nanoScroller({ preventPageScrolling: true });
              $("#artist_view").animate({left:'220', right:'0'},300);
              $("#artist_panel_hide").animate({left:'420', top:'145'},300);
             // $("#rightside").animate({right:'0',opacity:'1'},300);
},10);
    
    }
    function lPlaylists(){
        setTimeout(function() {
           // nano scroll bar start
      	      $(".nano").nanoScroller({ preventPageScrolling: true });
              $("#playlist_view").animate({left:'220', right:'0'},300);
              $("#playlist_panel_hide").animate({left:'420', top:'145'},300);
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
       
});

var type=0;
// bind search with keydown 



$(document).bind('keydown',function(e){
   if(!select){
 if(jQuery.inArray(e.keyCode,[8,9,13,16,17,18,19,20,32,33,34,35,36,37,38,39,40,45,46,91,92,93,107,109,112,113,114,115,116,117,118,119,120,121,122,123,144,145,224]) !== -1){ console.log('hehe             hehe'); return;}
   //check for escape key 
   if (e.keyCode == 27) { 
   if(type==1){
     type=0;
    $('#searchButton').addClass("notOpen");

    $("#searchDivcss").removeClass("searchLightboxOpen").addClass("searchLightboxClose");
   } 
   }//ecs
  else{
    
//starts

 if(type == 0){
    searchView(e);
    $('#searchBig').focus();
   
    }
    else{
        
        }


//ends
   }
      // $(document).unbind('keydown');
    // var duck=10;
   }
});


// search 
function searchView(e){
  if($('#searchButton').hasClass("notOpen")){
    // search icon css
    type=1;
    
     $('#searchButton').removeClass("notOpen");
   // alert(' open/visible ');
    // change the style of search div
    $("#searchDivcss").removeClass("searchLightboxClose").addClass("searchLightboxOpen");
    $('#searchBig').focus();
  }
  else{
    type=0;
    // search icon css
    // alert("not visible");
    $('#searchButton').addClass("notOpen");
    // active class on full search view only
    // change the style of search div
    $("#searchDivcss").removeClass("searchLightboxOpen").addClass("searchLightboxClose");
  }
}
