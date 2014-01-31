
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
 if(jQuery.inArray(e.keyCode,[8,9,13,16,17,18,19,20,32,33,34,35,36,37,38,39,40,45,46,91,92,93,107,109,112,113,114,115,116,117,118,119,120,121,122,123,144,145,224]) !== -1){ return;}
   //check for escape key 
   if (e.keyCode == 27) { 
   if(type==1){
     type=0;
    $('#searchButton').addClass("notOpen");
     $("#bigwrapper").removeClass("blur_back");
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
    //blur css
   $("#bigwrapper").addClass("blur_back");
 }
  else{
    type=0;
    // search icon css
    // alert("not visible");
    $('#searchButton').addClass("notOpen");
    // active class on full search view only
    // change the style of search div
    $("#searchDivcss").removeClass("searchLightboxOpen").addClass("searchLightboxClose");
   //blur css 
     $("#bigwrapper").removeClass("blur_back");
  }
}


/* draggable dropabble playqueue */

function add_queue_song(song)
{
  var id = 'song_'+song.id;
  var image = '\/songsmedia\/' + song.album.album_art;
  image = 'http://192.168.121.5:60000'+image;
  var artist_name = song.artists[0].artist;
  var song_name = song.song;
var html = '<div class="qimage" style="background:url(\''+image+'\'); background-size:cover">'
   + ' </div>'
   + '<div class="qinfo">'
   + '<div class="qsong">'+song_name+'</div>'
   + '<div class="qartist">'+artist_name+'</div></div>';
$( "<div class='qitem song' id='"+id+"'></div>" ).html( html ).appendTo( $("#popular_artists_list"));
$(".qsong").width($(".qitem").width()-50);
song_ready();
}

function add_queue(element)
{
var id='';
var image = '';
var artist_name = '';
var song_name = '';
var selected = $("#navigation").find("a.selected").attr('id');
if(selected == 'trending_link')
{
  id = element.attr('id');
  image = element.find('div.item').css('background-image');
  image = image.substring(4,image.length-1);
  artist_name = element.find('div.artist_name').text();
  song_name = element.find('div.song_name').text();

}

if(selected == 'artists_link')
{
  id = element.attr('id');
  image = element.parents().eq(3).find('img').attr('src');
  image = 'http://192.168.121.5:60000'+image;
  artist_name = element.parents().eq(5).find('div#artistName').text();
  song_name = element.find('div#p_song_name').text();

}

if(selected == 'albums_link')
{
  id = element.attr('id');
  image = element.parents().eq(3).find('img').attr('src');
  image = 'http://192.168.121.5:60000'+image;
  artist_name = element.parents().eq(3).find('div.artist').text();
  song_name = element.find('div#p_song_name').text();

}

var html = '<div class="qimage" style="background:url(\''+image+'\'); background-size:cover">'
   + ' </div>'
   + '<div class="qinfo">'
   + '<div class="qsong">'+song_name+'</div>'
   + '<div class="qartist">'+artist_name+'</div></div>';
$( "<div class='qitem song' id='"+id+"'></div>" ).html( html ).appendTo( $("#popular_artists_list"));
song_ready();
}


function dragging() {
   // $( "#catalog" ).accordion();
    $( ".draggable" ).draggable({
appendTo: "body",
helper: "clone"
});
    $( "#rightside" ).droppable({
activeClass: "ui-state-default",
hoverClass: "ui-state-hover",
accept: ".draggable",
drop: function( event, ui ) {
$( this ).find( ".placeholder" ).remove();
var element = ui.draggable;
add_queue(element);
}
}).sortable({
items: " div.qitem",
sort: function() {
// gets added unintentionally by droppable interacting with sortable
// using connectWithSortable fixes this, but doesn't allow you to customize active/hoverClass options
$( this ).removeClass( "ui-state-default" );
}
});

}


