/
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
/backup file of music.js  24-1 -2014 12.9am
