/* Base.js for basic javascript of jukebox*/
/*
   hash ={
   trending/[song/<id>]
   artists/[<id>/][song/<id>]
   albums/[<id>/][song/<id>]
   playlists/<username>/[<id>/][song/<id>]
   search/<search_string>[/song/<id>]
   }
*/
function bind_search_buttons(){

$("#search_song_count").bind('click',function(){
  $("#searchItemToShow>span").removeClass("search_active");
  $(this).addClass("search_active");
  search_full($('#inputFor').val());
});
$("#search_album_count").bind('click',function(){
  $("#searchItemToShow>span").removeClass("search_active");
  $(this).addClass("search_active");
  search_full($('#inputFor').val());
});
$("#search_artist_count").bind('click',function(){
  $("#searchItemToShow>span").removeClass("search_active");
  $(this).addClass("search_active");
  search_full($('#inputFor').val());
});
}

function search_full(search_str){

if(search_str === ""){

  $('#song_searchList').html('<div>Start typing to get results</div>');
 return;
}

$('#inputFor').val(search_str);
    $.get('search_all/',{q:search_str}, function(data){
            var songs = data;            // only songs coming for now
            if(songs.length >= 100) $('#search_song_count').html('Songs('+songs.length+'+)');
            else $('#search_song_count').html('Songs('+songs.length+')');



            if($('#search_song_count').hasClass("search_active")){
              $("#song_searchList").css({'display':'block'});
              $("#album_searchList").css({'display':'none'});
              $("#artist_searchList").css({'display':'none'});

            //by default clicked on songs
            $('#song_searchList').html($('#itemsDisplay').clone());
           // $('#centerdata').append('<div id="searchItemToShow"><span>Songs('+songs.length+')</span><span>Albums('+albums.length+')</span><span>Artists('+artists.length+')</span></div><div id="searchUnderline"></div></div>'+
       for(var i=0; i<songs.length;i++){
            if(songs[i].album.album_art=="") songs[i].album.album_art = 'albumart/default_'+Math.floor((Math.random() * 12) + 1)+'.jpg';

            var html =	'		<li>'+
		'			<div style="background-image:url('+'http://192.168.121.5\/songsmedia\/' + songs[i].album.album_art+')"  class="iDsrno"></div>'+
		'			<div class="iDname song draggable" id="song_'+songs[i].id+'">'+songs[i].song+'</div>'+
		'			<div class="iDalbum album" id="album_'+songs[i].album.id+'">'+songs[i].album.album+'</div>';
           if (banned_artists.indexOf(songs[i].artists[0].id) >= 0)
           {
              html += '	<div class="iDartist album" id="album_'+songs[i].album.id+'">'+songs[i].album.album+'</div>';
           }
           else
           {
              html += '	<div class="iDartist artist" id="artist_'+songs[i].artists[0].id+'">'+songs[i].artists[0].artist+'</div>';
           }

		       html += '</li>';
            $('#song_searchList').append(html);
        if(!(songs[i].id in songs_url)) songs_url[songs[i].id]=songs[i];
       }

      } // if end 
      else if($('#search_album_count').hasClass("search_active")){
        // alert("display albums");
              $("#song_searchList").css({'display':'none'});
              $("#album_searchList").css({'display':'block'});
              $("#artist_searchList").css({'display':'none'});
              var count = 0;

              for(var i in albums_json.English){
                
                if(albums_json.English[i].album.toLowerCase().indexOf(search_str.toLowerCase())>=0){
                  if(count>100) break;
                  count++;
              var album_name = albums_json.English[i].album;


               //by default clicked on songs
            $('#album_searchList').html('<li id="itemsDisplay">'+
    '     <div class="iDsrno" style="visibility:hidden;font-size: 12px;">99</div>'+
    '     <div class="iDname">NAME</div>'+
    '   </li>');
           // $('#centerdata').append('<div id="searchItemToShow"><span>Songs('+songs.length+')</span><span>Albums('+albums.length+')</span><span>Artists('+artists.length+')</span></div><div id="searchUnderline"></div></div>'+
    

            var html =  '<li>'+
    '     <div style="visibility:hidden;" class="iDsrno"></div>'+
    '     <div class="iDname album draggable" id="album_' +albums_json.Hindi[i].id+' ">'+album_name+'</div>';
           
           html += '</li>';
           


          }// if
          }//for

          // for hindi
          for(var i in albums_json.Hindi){
                
                if(albums_json.Hindi[i].album.toLowerCase().indexOf(search_str.toLowerCase())>=0){
                  if(count>100) break;
                  count++;
              var album_name = albums_json.Hindi[i].album;
             


               //by default clicked on songs
            // $('#album_searchList').html($('#itemsDisplay').clone());
           // $('#centerdata').append('<div id="searchItemToShow"><span>Songs('+songs.length+')</span><span>Albums('+albums.length+')</span><span>Artists('+artists.length+')</span></div><div id="searchUnderline"></div></div>'+
    

            html =  html + '<li>'+
    '     <div style="visibility:hidden;" class="iDsrno"></div>'+
    '     <div class="iDname album draggable" id="album_' +albums_json.Hindi[i].id+' ">'+album_name+'</div>';
           
           html += '</li>';
           


          }// if
          }//for

           if(count >= 100) $('#search_album_count').html('Albums(100+)');
            else $('#search_album_count').html('Albums('+count+')'); 
           $('#album_searchList').append(html);
      }
      else{
        alert("display artist");

              $("#song_searchList").css({'display':'none'});
              $("#album_searchList").css({'display':'none'});
              $("#artist_searchList").css({'display':'block'});

      }


//       debugger;
song_ready();
album_ready();
artist_ready();
dragging();
        });
}

function get_search_html(search_str)
{
    $('#centerdata').html(
      '<div id="searchViewOpened">'+
     '<div id="searchResultsFor">SEARCH RESULTS FOR</div>'+
     '<div id="inputSearchFor">'+
     '<input type="text" id="inputFor" />'+
     '</div>'+
     '<div>'
      );

$('#inputFor').focus(function() {
                     select = true;
                       }).blur(function(){
                     select = false;
                     });
$('#inputFor').val('');
$('#inputFor').val(search_str);
$('#inputFor').focus();
            $('#searchViewOpened').append('<div id="searchItemToShow"><span id="search_song_count" class="search_active">Songs(0)</span><span id="search_album_count">Albums(0)</span><span id="search_artist_count">Artists(0)</span></div><div id="searchUnderline"></div></div>'+
    '<div id="searchContentFull">'+
    '<ul class="searchList" id="song_searchList">'+
		'		<li id="itemsDisplay">'+
		'			<div class="iDsrno" style="visibility:hidden;font-size: 12px;">99</div>'+
		'			<div class="iDname">NAME</div>'+
		'			<div class="iDalbum">ALBUM</div>'+
		'			<div class="iDartist">ARTIST</div>'+
		'		</li>'+
    '</ul>'+
    '<ul class="searchList" id="album_searchList">'+
		'		<li id="itemsDisplay">'+
		'			<div class="iDsrno" style="visibility:hidden;font-size: 12px;">99</div>'+
		'			<div class="iDname">NAME</div>'+
		'			<div class="iDalbum">ARTIST</div>'+
		'			<div class="iDartist"></div>'+
		'		</li>'+
    '</ul>'+
    '<ul class="searchList" id="artist_searchList">'+
		'		<li id="itemsDisplay">'+
		'			<div class="iDsrno" style="visibility:hidden;font-size: 12px;">99</div>'+
		'			<div class="iDname">NAME</div>'+
		'			<div class="iDalbum"></div>'+
		'			<div class="iDartist"></div>'+
		'		</li>'+
    '</ul>'+
    '</div>'
    );
bind_search_buttons();
search_full(search_str);
$('#inputFor').on("keyup", function (event) {
    q = $(this).val();
    hash_change('search',q);

    // console.log('heree');
    //search_full(q);
});

}


function capitalize(s)
{
    return s[0].toUpperCase() + s.slice(1);
}

/*  -----------------------------  */
var prev_album = 'thers';
var albumtag_count=0;
var prev_artist = 'thers';
var artisttag_count=0;
var prev_hash="";
var albums_open=false;
var artists_open=false;
var playlists_open=false;
var public_playlists_open=false;
var trending_open=false;
var now_display='trending';
var albums_json = {};
var artists_json = {};
var playlists_json = {};
var public_playlists_json = {};
var trending_json={};
var queue = [];
var in_queue=false;
var songs_url = {};
var song_playing=0;
var login_cancel=false;
var default_language = 'English';
var banned_artists = [284,285];

if(logged_in=='True')
  logged_in = true;
else
  logged_in=false;
var adding_to_play = false;
var add_to_play = [];

$('#searchBig').bind("keyup", function (event) {
    q = $(this).val();
    //hash_change('search',q);
      if(q=='') 
      { 
        $("#startTyping").html("Start Typing...");
        $("#songSearch").empty();
        $("#albumSearch").empty();
        $("#artistSearch").empty();
        return;
      }
      else{
        $("#startTyping").html("Search results for")
      }
    search(q);
});
function search(q)
{
  if (q=='')
  {
    $("#songSearch").empty();
    $("#albumSearch").empty();
    $("#artistSearch").empty();
  }
  $.ajax({
      type: 'get',
      url: 'search?q='+q,
      success: function (data) {
       $("#songSearch").empty();
       $("#songSearch").append('<div class="searchHeading">SONGS<span> ('+data.songs[0]+')</span></div>');
       $("#songSearch").append('<div> <ul  id="songSearchSpan" class="searchResultList" > </ul> </div>');
       for(var i=0; i<data.songs[1].length; i++)
       {  
          if(data.songs[1][i].album.album_art=="") data.songs[1][i].album.album_art = 'albumart/default_'+Math.floor((Math.random() * 12) + 1)+'.jpg';

         var html = '<li class="song" id="song_'+data.songs[1][i].id+'"><div class="searchItemImg" style="background-image:url('+'http://192.168.121.5\/songsmedia\/' + data.songs[1][i].album.album_art+')" ></div>'
                  +  '<div class="searchItemDetails">'
		              +   '<div class="itemName">'+ data.songs[1][i].song+'</div>'
		              +    '<div class="itemSubDetail">'+data.songs[1][i].artists[0].artist+'</div></div></li>';
         $("#songSearchSpan").append(html);
         songs_url[data.songs[1][i].id]=data.songs[1][i];
       }
       $("#albumSearch").empty();
       $("#albumSearch").append('<div class="searchHeading">Albums<span> ('+data.albums[0]+')</span></div>');
       $("#albumSearch").append('<div> <ul  id="albumSearchSpan" class="searchResultList" > </ul> </div>');
       for(var i=0; i<data.albums[1].length; i++)
       {  
         if(data.albums[1][i].album_art=="") data.albums[1][i].album_art = 'albumart/default_'+Math.floor((Math.random() * 12) + 1)+'.jpg';

         var html = '<li class="album searchItem" id="album_'+data.albums[1][i].id+'"><div class="searchItemImg" style="background-image:url('+'http://192.168.121.5\/songsmedia\/' + data.albums[1][i].album_art+')" ></div>'
                  +  '<div class="searchItemDetails">'
		              +   '<div class="itemName">'+ data.albums[1][i].album+'</div>'
		              +    '<div class="itemSubDetail">'+data.albums[1][i].artists[0].artist+'</div></div></li>';
         $("#albumSearchSpan").append(html);
       }
       $("#artistSearch").empty();
       $("#artistSearch").append('<div class="searchHeading">Artists<span> ('+data.artists[0]+')</span></div>');
       $("#artistSearch").append('<div> <ul  id="artistSearchSpan" class="searchResultList" > </ul> </div>');
       for(var i=0; i<data.artists[1].length; i++)
       {
         var html = '<li class="artist searchItem" id="artist_'+data.artists[1][i].id+'"><div class="searchItemImg" style="background-image:url('+'http://192.168.121.5\/songsmedia\/' + data.artists[1][i].artist_art+')" ></div>'
                  +  '<div class="searchItemDetails">'
		              +   '<div class="itemName">'+ data.artists[1][i].artist+'</div>'
		              +    '</div></li>';
         $("#artistSearchSpan").append(html);
       }
      artist_ready();
      album_ready();
      song_ready();
      search_ready();
      hash = document.location.href.split('#')[1];
      if(!hash) hash="";
      hash = hash.split('/');
      }
    });
}





/************************************ Actual Work *******************************************/
// names-> for different urls working the same way
var names = {
  "trending" : ['trending/', 'get_song_html'],
  "albums" : ['albums/', 'get_album_html'],
  "artists" : ['artists/', 'get_artist_html']
};


function hash_change()
{
    hash = document.location.href.split('#')[1];
    if(!hash) hash="";
    hash = hash.split('/');
    song = hash.indexOf('song');
    var arg = $.map(arguments, function(value, index) {
          return [value];
          });
    if(song>=0 && arg[arg.length-2]!='song'){ arg.push('song'); arg.push(hash[song+1]); }
    document.location.href = "#" + arg.join('/');
}
// display function for display of list of either songs, artists or albums
function display(name){
  if (name in names){
    var items=[];

    if(name=='trending' && trending_open)
    {
      $("#centerdata").empty();
        items = trending_json; 
        $("#centerdata").append('<div id="trending_div"><div id="container"></div></div>');
        for (var i=0; i<items.length; i++){
		      $("#container").append(get_song_html(items[i]));
        }
        lTrending();
        dragging();
        options_binder();
        song_ready();
        trending_ready(); 
       $('.song_options').on('click',function(e) { 
       
       e.stopPropagation(); });
        return;
     }
    if(albums_open && name=='albums')
    {
      $("#centerdata").empty();
        items = albums_by_name; 
        $("#centerdata").append('<div id="albumsList">  <div class="nano" id="left_album_list">  <div id="contentList" style="padding-top:50px;"class="content"> </div></div></div>');
        $('#albumsList').append('<div id="language_options_div"><ul id="artist_language"><li>English</li><li>Hindi</li></ul></div><div id="albumContentSearch"><span id="searchIconTop"><i class="icon-search"></i></span><input type="text" id="dynamicSearch"></input></div>');
        for(var language in items)
        {
          if(language == default_language){
          // $('#artist_language').append('<option value="'+language+'" selected>'+language+'</option>');
          $('#artist_language li:nth-child(2)').removeClass('artist_language_selected');
          $('#artist_language li:nth-child(1)').removeClass().addClass('artist_language_selected');
          }
          else{
          $('#artist_language li:nth-child(2)').removeClass('artist_language_selected');
          $('#artist_language li:nth-child(1)').removeClass().addClass('artist_language_selected');

          // $('#artist_language').append('<option value="'+language+'">'+language+'</option>');
          }
        }
        language_binder();
        console.log(items[default_language].length);
        for (var i=0; i<albums_name[default_language].length; i++){
          get_album_html(albums_by_name[default_language][albums_name[default_language][i]]);
        }
        $("#albumsList").append('<div id="oneAlbumOpened"><div id="oaoWrapper"></div></div>');
        // $("#oneAlbumOpened").append('<div id="album_panel_hide"><i class="icon-reorder"></i></div>');
        lAlbums();
        album_ready();
        var aindex = window.location.hash.split('/');
        if(!(aindex.indexOf('#albums') + 1 < aindex.length  &&  !isNaN(aindex[aindex.indexOf('#albums') + 1])))
        $('#album_'+albums_by_name[default_language][albums_name[default_language][Math.floor((Math.random() * albums_name[default_language].length) + 1)]].id).click();
        return;
    }
    if(artists_open && name=='artists')
    {
      $("#centerdata").empty();
        items = artists_by_name;
        $("#centerdata").append('<div id="artistsList">  <div class="nano" id="left_album_list">  <div id="contentList" class="content" style="bottom: 68px;"> </div></div></div>');
        for (var i=0; i<artists_name.length; i++){
          if(banned_artists.indexOf(Number(artists_by_name[artists_name[i]].id)) >= 0){  continue; }
          get_artist_html(artists_by_name[artists_name[i]]);
        }
        $("#artistsList").append('<div id="artist_view"></div>');
        // $("#artistsList").append('<div id="artist_panel_hide"><i class="icon-reorder"></i></div>');
        lArtists();
        artist_ready();
        var aindex = window.location.hash.split('/');
        if(!(aindex.indexOf('#artists') + 1 < aindex.length  &&  !isNaN(aindex[aindex.indexOf('#artists') + 1])))
        $('#artist_'+artists_by_name[artists_name[Math.floor((Math.random() * artists_name.length) + 1)]].id).click();
       
        return;
    }
    // for hashtags
    var show = names[name];
    var url = show[0];
    var func = window[show[1]];
    $.ajax(url,contentType= "application/json").done( function(data){
      $("#centerdata").empty();
      if(name=='trending')
      {
        $("#centerdata").append('<div id="trending_div"><div id="container"></div></div>');
      }
      if(name=='albums')
      {
        $("#centerdata").append('<div id="albumsList">  <div class="nano" id="left_album_list">  <div id="contentList" style="padding-top:50px;" class="content"></div></div></div>');
      }
      if(name=='artists')
      {
        $("#centerdata").append('<div id="artistsList">  <div class="nano" id="left_album_list">  <div id="contentList" style="bottom: 68px;" class="content"></div></div></div>');
      }
      items=data;
      if(name!='albums'){
      for (var i=0; i<items.length; i++){
	      if(name=='trending')
	      {
		$("#container").append(func(items[i]));
	      }
        else if(name=='artists')
	      {
		      func(items[i]);
	      }
        else
        $("#centerdata").append(func(items[i]));
      }}
      else
      {
        $('#albumsList').append('<div id="language_options_div"><ul id="artist_language"><li>English</li><li>Hindi</li></ul></div><div id="albumContentSearch"><span id="searchIconTop"><i class="icon-search"></i></span><input type="text" id="dynamicSearch"></input></div>');
        for(var language in items)
        {
          if(language == default_language){
          $('#artist_language li:nth-child(2)').removeClass('artist_language_selected');
          $('#artist_language li:nth-child(1)').removeClass().addClass('artist_language_selected');
          }
          else{
          $('#artist_language li:nth-child(2)').removeClass('artist_language_selected');
          $('#artist_language li:nth-child(1)').removeClass().addClass('artist_language_selected');
          }
        }
        for (var i=0; i<items[default_language].length; i++){
          get_album_html(items[default_language][i]);
        }
        language_binder();
      }
      artist_ready();
      album_ready();
      song_ready();
    
      if(name=='trending')
      {
   //     $("#centerdata").append('</div></div>');
        lTrending();
        dragging();
        options_binder();
        trending_ready(); 
        trending_json = items;
        trending_open=true;

        $('.song_options').on('click',function(e) { 
       
       e.stopPropagation(); });
      }
      if(name=='albums')
      {
       // $("#centerdata").append('</div></div></div>');
        $("#albumsList").append('<div id="oneAlbumOpened"><div id="oaoWrapper"></div></div>');
        // $("#oneAlbumOpened").append('<div id="album_panel_hide"><i class="icon-reorder"></i></div>');
        lAlbums();
        albums_open = true;
        $('#album_'+albums_by_name[default_language][albums_name[default_language][Math.floor((Math.random() * albums_name[default_language].length) + 1)]].id).click();
      }
      if(name=='artists')
      {
       // $("#centerdata").append('</div></div></div>');
        $("#artistsList").append('<div id="artist_view"></div>');
        // $("#artistsList").append('<div id="artist_panel_hide"><i class="icon-reorder"></i></div>');
        lArtists();
        artists_json = items;
        artists_open = true;
        $('#artist_'+artists_by_name[artists_name[Math.floor((Math.random() * artists_name.length) + 1)]].id).click();
      }
    });
  }
}


// display_album for displaying a specific album
function display_album(id){
  url = "albums/" + id;
    if(id in albums_json1)
    {
      var album = albums_json1[id];
      $("#oaoWrapper").empty();
      $("#oaoWrapper").append('<div id="oaoLeft"></div>    <div id="oaoRight"> <div id="popular_list"></div> </div>');
      if(album.album_art=="") album.album_art = 'albumart/default_'+Math.floor((Math.random() * 12) + 1)+'.jpg';
      $("#oaoLeft").append('<img class="albumImage album draggable" src="http://192.168.121.5/songsmedia/'+ album.album_art +'"  style="display:block;"></img>');  // change the css accordingly
      $("#oaoLeft").append('<div id="oaoLInfo"> <div class="playable">'+album.album+'</div> </div>');
   //   html = "<br> Album Name: <br>" + album.album + "<br> Artists: ";
      if (banned_artists.indexOf(album.artists[0].id) < 0)
          $('#oaoLInfo').append("<div class='artist' id='artist_"+album.artists[0].id+"'>" + album.artists[0].artist + "</div> ");
      html = '<ul>';
      for(var j=0; j<album.song_set.length; j++)
      {
         var k = album.song_set[j].id;
       // html += "" + album.song_set[j].song + "<br> ";
        html += '<li class="popular_item song draggable" id="song_'+k+'"><div class="list_icon"><i class="icon-play list_icon_play"></i></div><div id="list_number">'+left_add_zero(j+1)+'</div>  <div id="p_song_name"><span class="song_in_span">'+album.song_set[j].song +'</span></div><div class="album_options"><i class="album_options_button icon-ellipsis-horizontal"></i><div class="album_item_setting_box"><ul><li class="song" id="song_'+k+'">Play now</li><li class="next" id="next_'+k+'">Play next</li><li class="last" id="last_'+k+'">Play last</li><li class="options_add_to_playlist" id="add_'+k+'">Add to playlist</li><li class="share_url" id="share_'+k+'">Share</li></ul></div></div>';
        if(!(album.song_set[j].id in songs_url)) songs_url[album.song_set[j].id]=album.song_set[j];

      }
      $("#popular_list").append(html);

      artist_ready();
      dragging();
      song_ready();
      albums_song_options_binder();
      options_binder();
      return;
    }
    $.ajax(url,contentType= "application/json").done( function(data){
      var album = data;
      $("#oaoWrapper").empty();
      $("#oaoWrapper").append('<div id="oaoLeft"></div>    <div id="oaoRight"> <div id="popular_list"></div> </div>');
      if(album.album_art=="") album.album_art = 'albumart/default_'+Math.floor((Math.random() * 12) + 1)+'.jpg';
      $("#oaoLeft").append('<img class="albumImage album draggable" src="http://192.168.121.5/songsmedia/'+ album.album_art +'"  style="display:block;"></img>');  // change the css accordingly
      $("#oaoLeft").append('<div id="oaoLInfo"> <div class="playable">'+album.album+'</div> </div>');
   //   html = "<br> Album Name: <br>" + album.album + "<br> Artists: ";
      if (banned_artists.indexOf(album.artists[0].id) < 0)
          $('#oaoLInfo').append("<div class='artist' id='artist_"+album.artists[0].id+"'>" + album.artists[0].artist + "</div> ");
      html = '<ul>';
      for(var j=0; j<album.song_set.length; j++)
      {
         var k = album.song_set[j].id;
       // html += "" + album.song_set[j].song + "<br> ";
        html += '<li class="popular_item song draggable" id="song_'+k+'"><div class="list_icon"><i class="icon-play list_icon_play"></i></div><div id="list_number">'+left_add_zero(j+1)+'</div>  <div id="p_song_name"><span class="song_in_span">'+album.song_set[j].song +'</span></div><div class="album_options"><i class="album_options_button icon-ellipsis-horizontal"></i><div class="album_item_setting_box"><ul><li class="song" id="song_'+k+'">Play now</li><li class="next" id="next_'+k+'">Play next</li><li class="last" id="last_'+k+'">Play last</li><li class="options_add_to_playlist" id="add_'+k+'">Add to playlist</li><li class="share_url" id="share_'+k+'">Share</li></ul></div></div>';
        if(!(album.song_set[j].id in songs_url)) songs_url[album.song_set[j].id]=album.song_set[j];

      }
      $("#popular_list").append(html);

      artist_ready();
      dragging();
      song_ready();
      albums_song_options_binder();
      options_binder();
    });

}

function left_add_zero(n){
      return n > 9 ? "" + n: "0" + n;
}

// display_artist for displaying a specific artist
function display_artist(id){
  if(banned_artists.indexOf(id)>=0) return;
  if(id in artists_json1)
  {
      var artist = artists_json1[id];
      $("#artist_view").empty();
      $("#artist_view").append('<div id="artist_banner" style="background:url('+'\'http://192.168.121.5\/songsmedia\/' + artist.cover_pic +  '\'); background-size:cover; "></div>');
  //    debugger;
      $("#artist_banner").append('<div id="layer" style="background:url(\'\/static/images/jukebox/gradientCover.png\'); " ></div>');
      $("#artist_banner").append('<div id="artistInfo"><div id="artistName">'+artist.artist+'</div><div id="artistAlbumCount">'+artist.album_set.length+' Albums</div></div>');
      $("#artist_view").append('<div id="artist_body"></div>');
      for(var j=0; j<artist.album_set.length; j++)
      { if(artist.album_set[j].album_art=="") artist.album_set[j].album_art = 'albumart/default_'+Math.floor((Math.random() * 12) + 1)+'.jpg';
        html = '<div class="artist_album">'
                + '<div class="artist_album_pic album draggable"><img src="http://192.168.121.5/songsmedia/'+ artist.album_set[j].album_art +'"></img></div>'
                + '<div id="popular_heading"> '+artist.album_set[j].album+' </div>'
                + '<div id="artist_song_list">'
                + '<div id="popular_list">'
                + '<ul>';

      for(var k=0; k<artist.album_set[j].song_set.length; k++)
      {
        var l = artist.album_set[j].song_set[k].id;

       // html += "" + album.song_set[j].song + "<br> ";
        html += '<li class=" song popular_item draggable" id="song_'+l+'"><div class="list_icon"><i class="icon-play list_icon_play"></i></div><div id="list_number">'+left_add_zero(k+1)+'</div> <div id="p_song_name"><span class="song_in_span">'+ artist.album_set[j].song_set[k].song +'</span></div><div class="artist_options"><i class="artist_options_button icon-ellipsis-horizontal"></i><div class="artist_item_setting_box"><ul><li class="song" id="song_'+l+'">Play now</li><li class="next" id="next_'+l+'">Play next</li><li class="last" id="last_'+l+'">Play last</li><li class="options_add_to_playlist" id="add_'+l+'">Add to playlist</li><li class="share_url" id="share_'+l+'">Share</li></ul></div></div>';
        if(!(artist.album_set[j].song_set[k].id in songs_url)) songs_url[artist.album_set[j].song_set[k].id]=artist.album_set[j].song_set[k];

      }

        html +='</ul>'
                + '</div>'
                + '</div>'
                +'</div>';
        $("#artist_body").append(html);
       // $("#artist_album").append('<div class="artist_album_pic"><img src="/media/'+ artist.album_set[j].album_art +'"></img></div>');
      }
     /* debugger;
      html = "<br> Artist: <br>" +
        "Artist Name: " + artist.artist +
        "<br> <img src='/media/"+ artist.cover_pic + "' width='300px' height='300px'> <br> <br>" +
        "Albums: " + artist.album_set.length + "<br>";
      for(var j=0; j<artist.album_set.length; j++)
      {
        k = artist.album_set[j].id;
        html += "<div class='album' id='album_"+k+"'>" + artist.album_set[j].album +
        "<br> <img src='/media/"+ artist.album_set[j].album_art + "' width='100px' height='100px'> <br>" ;
      }
      $("#append").append(html);
      */
      album_ready();
      dragging();
      song_ready();
      artist_song_options_binder();
      options_binder();
      artist_language_dialog_binder();
      $('body').scrollTop(100);


       //to adjust the height of artist image
      var widArtistDiv = $('#artist_banner').width();
      var heiArtistDiv = (widArtistDiv*3)/9;
      $('#artist_banner').css({
         'height' : heiArtistDiv
         });

      var shaddow = heiArtistDiv - 95;
       $('#layer').css({
         'top' : shaddow
         });

      var textArtist = heiArtistDiv - 49;
      $('#artistInfo').css({
         'top' : textArtist
         });


      $('body').animate({scrollTop:0}, '500', 'swing', function() { 
     $(document).scroll(function () { 

       $('#artist_body').css({
         'top' : -($(this).scrollTop()/1.4)+"px"
         }); 

       $('#artistInfo').css({
         'top' : -($(this).scrollTop()/1.4)+textArtist+"px"
         }); 
       $('#layer').css({
         'top' : -($(this).scrollTop()/1.4)+shaddow+"px"
         }); 

       }); 
           });

     
      /*smooth scrolling enable only on atist_view */
     $('#artist_view').smoothWheel({refer:"body"});
     $('#sidebar').smoothWheel({refer:"body"});
     $('#bottom').smoothWheel({refer:"body"});


  }
  url = "artists/" + id;
    $.ajax(url,contentType= "application/json").done( function(data){
      var artist = data;
      $("#artist_view").empty();
      $("#artist_view").append('<div id="artist_banner" style="background:url('+'\'http://192.168.121.5\/songsmedia\/' + artist.cover_pic +  '\'); background-size:cover; "></div>');
  //    debugger;
      $("#artist_banner").append('<div id="layer" style="background:url(\'\/static/images/jukebox/gradientCover.png\'); " ></div>');
      $("#artist_banner").append('<div id="artistInfo"><div id="artistName">'+artist.artist+'</div><div id="artistAlbumCount">'+artist.album_set.length+' Albums</div></div>');
      $("#artist_view").append('<div id="artist_body"></div>');
      for(var j=0; j<artist.album_set.length; j++)
      { if(artist.album_set[j].album_art=="") artist.album_set[j].album_art = 'albumart/default_'+Math.floor((Math.random() * 12) + 1)+'.jpg';
        html = '<div class="artist_album">'
                + '<div class="artist_album_pic album draggable"><img src="http://192.168.121.5/songsmedia/'+ artist.album_set[j].album_art +'"></img></div>'
                + '<div id="popular_heading"> '+artist.album_set[j].album+' </div>'
                + '<div id="artist_song_list">'
                + '<div id="popular_list">'
                + '<ul>';

      for(var k=0; k<artist.album_set[j].song_set.length; k++)
      {
        var l = artist.album_set[j].song_set[k].id;

       // html += "" + album.song_set[j].song + "<br> ";
        html += '<li class=" song popular_item draggable" id="song_'+l+'"><div class="list_icon"><i class="icon-play list_icon_play"></i></div><div id="list_number">'+left_add_zero(k+1)+'</div> <div id="p_song_name"><span class="song_in_span">'+ artist.album_set[j].song_set[k].song +'</span></div><div class="artist_options"><i class="artist_options_button icon-ellipsis-horizontal"></i><div class="artist_item_setting_box"><ul><li class="song" id="song_'+l+'">Play now</li><li class="next" id="next_'+l+'">Play next</li><li class="last" id="last_'+l+'">Play last</li><li class="options_add_to_playlist" id="add_'+l+'">Add to playlist</li><li class="share_url" id="share_'+l+'">Share</li></ul></div></div>';
        if(!(artist.album_set[j].song_set[k].id in songs_url)) songs_url[artist.album_set[j].song_set[k].id]=artist.album_set[j].song_set[k];

      }

        html +='</ul>'
                + '</div>'
                + '</div>'
                +'</div>';
        $("#artist_body").append(html);
       // $("#artist_album").append('<div class="artist_album_pic"><img src="/media/'+ artist.album_set[j].album_art +'"></img></div>');
      }
     /* debugger;
      html = "<br> Artist: <br>" +
        "Artist Name: " + artist.artist +
        "<br> <img src='/media/"+ artist.cover_pic + "' width='300px' height='300px'> <br> <br>" +
        "Albums: " + artist.album_set.length + "<br>";
      for(var j=0; j<artist.album_set.length; j++)
      {
        k = artist.album_set[j].id;
        html += "<div class='album' id='album_"+k+"'>" + artist.album_set[j].album +
        "<br> <img src='/media/"+ artist.album_set[j].album_art + "' width='100px' height='100px'> <br>" ;
      }
      $("#append").append(html);
      */
      album_ready();
      dragging();
      song_ready();
      artist_song_options_binder();
      options_binder();
      artist_language_dialog_binder();
      $('body').scrollTop(100);


       //to adjust the height of artist image
      var widArtistDiv = $('#artist_banner').width();
      var heiArtistDiv = (widArtistDiv*3)/9;
      $('#artist_banner').css({
         'height' : heiArtistDiv
         });

      var shaddow = heiArtistDiv - 95;
       $('#layer').css({
         'top' : shaddow
         });

      var textArtist = heiArtistDiv - 49;
      $('#artistInfo').css({
         'top' : textArtist
         });


      $('body').animate({scrollTop:0}, '500', 'swing', function() { 
     $(document).scroll(function () { 

       $('#artist_body').css({
         'top' : -($(this).scrollTop()/1.4)+"px"
         }); 

       $('#artistInfo').css({
         'top' : -($(this).scrollTop()/1.4)+textArtist+"px"
         }); 
       $('#layer').css({
         'top' : -($(this).scrollTop()/1.4)+shaddow+"px"
         }); 

       }); 
           });

     
      /*smooth scrolling enable only on atist_view */
     $('#artist_view').smoothWheel({refer:"body"});
     $('#sidebar').smoothWheel({refer:"body"});
     $('#bottom').smoothWheel({refer:"body"});


    });

}


/*
var load_playQueue = function(){
      $('#playQueue').empty();
      $('#qList').html('<div class="qitem"><div class="qimage"></div><div class="qinfo"><div class="qsong">Diamonds</div><div class="qartist">Rihanna</div></div></div>');
}

*/









var select = false;

var create_playlist = function() {
 
      $("#playlist_new").empty();
      $("#playlist_new").html('<div id="plus_icon"><i id="icon-remove-color" class="icon-remove"></i></div><input placeholder="Playlist name" type="text" id="create_new_play"></input>').find('#create_new_play').animate({opacity:'1'});
      $("#create_new_play").focus();
      select = true;
      $('#create_new_play').keypress(function(e) {
            if (e.which == 13) {
                    var val = $("#create_new_play").val();
                   // alert(val);
                   // if(val){
                    var html = $('#playlists').html();
                    $('#playlists').prepend('<li class="playlist" id="temp" ><span >'+val+'</span></li>');
                   // $('#playlist_new').empty();
                     $('#playlist_new').html('<div id="plus_icon"><i class="icon-plus"></i></div><div id="create_new_div"><a id="create_new">Create New</a></div>');
                   /*  $.ajax({
                        type: 'post',
                        url: 'playlist/',
                        data: {'name':val} 
                       });
                     */
                   $.post('playlists/',{name:val}, function(data){
                         $('#temp').attr('id','playlist_'+data.id);
                         playlist_ready();
                         get_json('playlists');
                     });  
                     val=null;

                     //   }
                     $("#playlist_new").bind("click",create_playlist);
                        }
                       
                        });
      $('#create_new_play').focus(function() {
                     select = true;
                       }).blur(function(){
                     select = false;

                   $('#playlist_new').html('<div id="plus_icon"><i class="icon-plus"></i></div><div id="create_new_div"><a id="create_new">Create New</a></div>');
                    $("#playlist_new").bind("click",create_playlist);

                        });
          }



function display_playlists(){
      if(!logged_in)
      {
        $('#signin_button').click();
        return;
      }
      $("#centerdata").empty();
        $("#centerdata").append('<div id="playlistsList">  <div class="nano" id="left_playlist_list">  <div id="contentList" class="content"> </div></div></div>');
  if( playlists_open )
  {
      var data = playlists_json;
      if(data.active)
      {
        var html = '<div class="start"><div class="list_alpha"><div class="playlist_create" id="playlist_new"><div id="plus_icon"><i class="icon-plus"></i></div><div id="create_new_div"><a id="create_new">Create New</a></div></div> <ul id= "playlists"></ul></div></div>';
      $("#contentList").append(html);
      for(var i=0; i<data.playlists.length; i++){
        var playlist = data.playlists[i];
        $("#playlists").append('<li class="playlist" id="playlist_'+ playlist.id +'"><span>'+playlist.name+'</span></li>');
      }
          $("#playlistsList").append('<div id="playlist_view"></div>');
          $("#playlistsList").append('<div id="playlist_panel_hide"><i class="icon-reorder"></i></div>');
          lPlaylists();
      $("#playlist_new").bind("click",create_playlist);
      playlist_ready();
    }
    else
    {
      $("#contentList").append('Login Required');
    return;
    }

  }
  else{
  url = 'playlists/';
  $.ajax(url,{ type:"GET" } ,contentType= "application/json").done( function(data){
      $("#centerdata").empty();
        $("#centerdata").append('<div id="playlistsList">  <div class="nano" id="left_playlist_list">  <div id="contentList" class="content"> </div></div></div>');
      if(data.active)
      {
        html = '<div class="start"><div class="list_alpha"><div class="playlist_create" id="playlist_new"><div id="plus_icon"><i class="icon-plus"></i></div><div id="create_new_div"><a id="create_new">Create New</a></div></div> <ul id= "playlists"></ul></div></div>';
      $("#contentList").append(html);
      for(var i=0; i<data.playlists.length; i++){
        var playlist = data.playlists[i];
        $("#playlists").append('<li class="playlist" id="playlist_'+ playlist.id +'"><span>'+playlist.name+'</span></li>');
      }
          $("#playlistsList").append('<div id="playlist_view"></div>');
          $("#playlistsList").append('<div id="playlist_panel_hide"><i class="icon-reorder"></i></div>');
          lPlaylists();
      $("#playlist_new").bind("click",create_playlist);
      playlist_ready();
      playlists_json=data;
      playlists_open=true;
    }
    else
    {
       
      $("#contentList").append('Login Required');
    }
    $("#create_new").on('click',function(){
      alert('sad');
      $("#playlist_new").empty();
      $("#playlist_new").html('<input type="text" id="create_new_play"></input>');
      $("#create_new_play").focus();
      select = true;
      $('#create_new_play').keypress(function(e) {
            if (e.which == 13) {
                    var val = $("#create_new_play").val();
                   // alert(val);
                   // if(val){
                    $('#playlists').append('<li><span>'+val+'</span></li>');
                   // $('#playlist_new').empty();
                    $('#playlist_new').html('<a id="create_new">+ Create New</a>');
                        val=null;
                     //   }
                        }
                       
                        });
            $('#create_new_play').focus(function() {
                      select = true;
                      
                          }).blur(function(){
                                  select = false;
                                        });
    }); 
    /**/
  });
  }
}
var playlist_open_now=[];
function display_playlist(id){
  var play_id = id;
  url = "playlists/" + id;
    $.ajax(url,contentType= "application/json").done( function(data){
        if('detail' in data && data['detail']=='Not found')
        {
          alert('Not yours');
          return;
        }
        if(data['songs']=='')
        {
          alert('Empty');
          return;
        }
      var playlist = data;
      var banner_songs_array = [];
      var album_present = [];
      playlist_open_now = [];
      var usong_count=0;
      var songs = playlist.songs.split('b');
      var public_str = "Private";
      if(playlist.private)
      {
          public_str = "Public";
      }
      var owner_str = '<option value="add_to_queue">Add To Queue</option>';
      if(playlist.owner===true)
      {
          owner_str +=
              '<option value="delete_'+play_id+'">Delete</option>'+
              '<option value="rename_'+play_id+'">Rename</option>'+
              '<option id="public_toggle" value="publicToggle_'+play_id+'">Make '+public_str+'</option>';
      }

          html = '<div id="playlistInfo"><div id="playlistName">'+playlist.name;
          pop = playlist.owner;
          if(!playlist.private && playlist.owner!==true) html += ' by '+ playlist.owner;
          html +='</div><div id="playlistSongCount">'+
          '<div id="playlist_option_icon" class="icon-ellipsis-horizontal"></div>'+
            '<select id="playlist_options">'+
              '<option value="default">---</option>'+
               owner_str +
            '</select>'+
          songs.length+' Songs</div></div>';
      $("#playlist_view").empty();
      $("#playlist_view").append('<div id="playlistBanner"></div>');
  //    debugger;
      $("#playlistBanner").append('<div id="layerBanner" style="background:url(\'\/static/images/jukebox/gradientCover.png\'); " ></div>');
      $("#playlistBanner").append('<ul><li></li><li></li><li></li><li></li><li></li></ul>');
      $("#playlistBanner").append(html);
      $("#playlist_view").append('<div id="viewPlaylist"><div id="playlistContentFull"></div></div>');
      var html = '<ul id="play_sortable">';
      for(var j=0; j<songs.length; j++)
      {
        var k = playlist.songs_list[parseInt(songs[j])].id;
        var id = 'song_'+k;
        var image = playlist.songs_list[parseInt(songs[j])].album.album_art;
        if(image=="") image = 'albumart/default_'+Math.floor((Math.random() * 12) + 1)+'.jpg';
        image = 'http://192.168.121.5/songsmedia/'+image;
        var artist_name = playlist.songs_list[parseInt(songs[j])].artists[0].artist;
        var album_name = playlist.songs_list[parseInt(songs[j])].album.album;
        var song_name = playlist.songs_list[parseInt(songs[j])].song;
        var artist_id = playlist.songs_list[parseInt(songs[j])].artists[0].id;
        var album_id = playlist.songs_list[parseInt(songs[j])].album.id;
        var file_name = playlist.songs_list[parseInt(songs[j])].file_name;
        //'<div class="pqimage" style="background:url(\''+image+'\'); background-size:cover">'

       if (banned_artists.indexOf(artist_id) >= 0)
        html += '<li ><div class="iDsrno" style="background-image:url('+ image+')"></div><div class="iDname song draggable" id="'+id+'">'+song_name+'</div><div class="iDalbum album" id="album_'+album_id+'">'+album_name+'</div><div class="iDartist album" id="album_'+album_id+'">'+album_name+'</div id="iDoptions"><div class="iDoptions"><i id="playlist_setting_icon" class="icon-ellipsis-horizontal"></i><div class="playlist_item_setting_box"><ul><li class="song" id="song_'+k+'">Play now</li><li class="next" id="next_'+k+'">Play next</li><li class="last" id="last_'+k+'">Play last</li><li class="options_add_to_playlist" id="add_'+k+'">Add to playlist</li><li class="share_url" id="share_'+k+'">Share</li><li class="delete_from_playlist" id="delete_'+j+'_'+play_id+'">Delete</li></ul></div></div></li>';
       else
        html += '<li ><div class="iDsrno" style="background-image:url('+ image+')"></div><div class="iDname song draggable" id="'+id+'">'+song_name+'</div><div class="iDalbum album" id="album_'+album_id+'">'+album_name+'</div><div class="iDartist artist" id="artist_'+artist_id+'">'+artist_name+'</div id="iDoptions"><div class="iDoptions"><i id="playlist_setting_icon" class="icon-ellipsis-horizontal"></i><div class="playlist_item_setting_box"><ul><li class="song" id="song_'+k+'">Play now</li><li class="next" id="next_'+k+'">Play next</li><li class="last" id="last_'+k+'">Play last</li><li class="options_add_to_playlist" id="add_'+k+'">Add to playlist</li><li class="share_url" id="share_'+k+'">Share</li><li class="delete_from_playlist" id="delete_'+j+'_'+play_id+'">Delete</li></ul></div></div></li>';
        if(!(playlist.songs_list[parseInt(songs[j])].id in songs_url)) songs_url[playlist.songs_list[parseInt(songs[j])].id]=playlist.songs_list[parseInt(songs[j])];
        playlist_open_now.push(playlist.songs_list[parseInt(songs[j])]);
        if($.inArray(album_id,album_present)>=0) continue;
        banner_songs_array[usong_count++]=k;
        album_present.push(album_id);
      }
      html +='</ul>';
      $('#playlistContentFull').append(html);

       var widthOfDiv = $('#playlist_view').width()/5;
       $('#playlistBanner ul li').css({width:widthOfDiv,height:widthOfDiv});
       $('#playlistBanner').css({height:widthOfDiv});
       $('#layerBanner').css({top:widthOfDiv-100+5});
        $("#playlistInfo").css({top:widthOfDiv-100+5+50});


      playlist_banner_images(banner_songs_array);
      album_ready();
      artist_ready();
      song_ready();
      dragging();
      playlist_song_options_binder(play_id, playlist.owner);
      options_binder();
      playlist_options_binder();
    });
}


// for 1 song html
function get_song_html(song)
{
  var album=song.album;
  var album_art;
  if(album){ album_art = album.album_art; album= album.album; }
  else{ album=" "; album_art=" ";}
  if(album_art=="") album_art = 'albumart/default_'+Math.floor((Math.random() * 12) + 1)+'.jpg';
  var k=song.id;
/*  html = "<br> Song: "+ song.song+ "<br> Album: " + album +"<br> Artist: ";
  for (var j=0; j<song.artists.length; j++)
  {
    html += song.artists[j].artist + ", ";
  }
*/
/*  html += "<br> Count: <p id='count_"+k+"'>" + song.count + "</p> " +
    "<img src=\'\/media\/" + album_art + "\' width='300px' height='300px'>" +
    "<br> <span class='song' id='song_" + k + "'>Play </span> <br><br>";
*/
  var html1 = "<div class='item_wrapper song playable draggable' id='song_"+k+"' data-type='play' data-value='"+k+"'>"+
    '<div class="item"  id="song_'+k+'" style="background:url('+'\'http://192.168.121.5\/songsmedia\/' + album_art +  '\'); background-size:cover">' +
   '<div class="song_options">' +
   '<i class="icon-ellipsis-horizontal setting_button"></i>' +
   '<div class="song_setting_box">'+
   '<ul><li class="song_div song" id="song_'+k+'">Play Now</li>' +
   '<li class="song_div next" id="next_'+k+'">Play Next</li>' +
   '<li class="song_div last" id="last_'+k+'">Play Last</li>'+
   '<li class="song_div options_add_to_playlist" id="add_'+k+'">Add to Playlist</li>'+
   '<li class="song_div share_url" id="share_'+k+'">Share</li></ul>'+
   '</div></div>'+
   ' <div class="faint"></div>'+
   ' <a class="play_icon"><img src="../static/images/jukebox/icon_new_play.png" width="50px" height="50px"></a>'+
   ' </div>' +
   ' <div class="artist_data">' +
   ' <div class="details">' +
   ' <div class="song_name">' + song.song + '</div>' +
   ' <div class="artist_name">';  
  if (banned_artists.indexOf(song.artists[0].id) >= 0)
  {
    html1 += song.album.album;
  }
  else
  {
    html1 += song.artists[0].artist;
  }
   html1 += '</div>'+
    '</div>' +
    '</div>';
    
  html = html1
  return html;
}



// for 1 artist html
function get_artist_html(artist)
{
  /*html = "<div class='artist' id='artist_"+artist.id+"'>" +
    "<br> Artist: "+ artist.artist +
    "<br> <img src='/media/" + artist.cover_pic + "' width='1000px' height='400px'>" +
    "<br><br><br></div>";
  return html;
*/
  html = "";
  tagg = '#';
  if(!artist.artist) return;
  var name = capitalize(artist.artist);
  if(!name[0].match(/^[A-Z]+$/)) tagg='#';
  else tagg=name[0];

  if(prev_artist!=tagg)
  {
    artisttag_count++;
   // html += '</ul></div></div>';
    html += '<div class="start">'+
             '<div class="head_alpha">'+tagg+'</div>'+
             '<div class="head_border"></div>'+
              '<div class="list_alpha"> <ul id="artist_tag_'+artisttag_count+'"></ul></div></div>';
    $("#contentList").append(html);
   prev_artist=tagg;
  }
 // html +=  "<span class='artist' id='artist_"+ artist.id +"'>" +
  //  "<li> "+ name + '</li></span>';
 // html += "<li>"+name+"</li>";
  artisttag_id = "#artist_tag_"+artisttag_count;
  $(artisttag_id).append('<li class="artist" id="artist_'+ artist.id +'"><span>'+name+'</span></li>');
}

// for 1 album html
function get_album_html(album)
{
  html = "";
  tagg = '#';
  if(!album.album) return;
  var name = capitalize(album.album);
  if(!name[0].match(/^[A-Z]+$/)) tagg='#';
  else tagg=name[0];

  if(prev_album!=tagg)
  {
    albumtag_count++;
   // html += '</ul></div></div>';
    html += '<div class="start">'+
             '<div class="head_alpha">'+tagg+'</div>'+
             '<div class="head_border"></div>'+
              '<div class="list_alpha"> <ul id="album_tag_'+albumtag_count+'"></ul></div></div>';
    $("#contentList").append(html);
   prev_album=tagg;
  }
 // html +=  "<span class='album' id='album_"+ album.id +"'>" +
  //  "<li> "+ name + '</li></span>';
 // html += "<li>"+name+"</li>";
  albumtag_id = "#album_tag_"+albumtag_count;
  $(albumtag_id).append('<li class="album" id="album_'+ album.id +'"><span >'+name+'</span></li>');
/*
  for (var j=0; j<album.artists.length; j++)
  {
    html +=  album.artists[j].artist + ", ";
  }
    html += "<br> <img src=\'\/media\/" + album.album_art + "\' width='300px' height='300px'>" +
    "<br><br><br>";
*/
  //return html;
}

function count_increase(id)
{
    var url = 'play?song_id='+id;
    $.ajax(url,contentType= "application/json").done( function(){console.log('yoooo');} );
}


var interval;

function play(id)
{
  if(id in songs_url){
    var song = songs_url[id];
    $('#song_'+song_playing).find('.faint').attr('style','');
    $('#song_'+song_playing).find('.play_icon').attr('style','');
    Jukebox.play_url('song_'+id,'http://192.168.121.5/songs/english/'+song.file_name);
    if( !in_queue && (id != song_playing)){ add_queue_song(song); now_playing=queue.length-1; }
    $("#musicPlayerPic").empty();
    $('#mini_image').css({'margin-top':'150px'});
    // alert('ssss');
    if(song.album.album_art=="") song.album.album_art = 'albumart/default_'+Math.floor((Math.random() * 12) + 1)+'.jpg';
    $("#mini_image").css({'background-image':'url('+'http://192.168.121.5\/songsmedia\/' + song.album.album_art+')'});
    $('#mini_image').animate({marginTop:'0px'});
//   $("#musicPlayerPic").append('<img src="\/songsmedia\/' + song.album.album_art +  '" style="width: 32px; height: 32px;" >');
//   Jukebox.play_url('song_'+id,'http://192.168.121.5/songs/english/'+song.file_name)
 $("#ilSong").html('<b>'+song.song+'</b>');
  var art = [];
  for(var i=0;i<song.artists.length && i<5; i++) art.push(song.artists[i].artist);
  $("#ilArtist").html('- '+art.join(' ,'));
   // $(song_id).html(song.count);
    song_playing = id;
    clearTimeout(interval);
    interval = setTimeout(function(){ count_increase(id); },5000);
    }
  else
  {
    var url = "song/" + id;
    $.ajax(url,contentType= "application/json").done( function(data){
       var song = data;
        if( !in_queue && (id != song_playing)){ add_queue_song(song); now_playing=queue.length-1; }
        $("#musicPlayerPic").empty();
         $('#mini_image').css({'margin-top':'150px'});
        if(song.album.album_art=="") song.album.album_art = 'albumart/default_'+Math.floor((Math.random() * 12) + 1)+'.jpg';

        $("#mini_image").css({'background-image':'url('+'http://192.168.121.5\/songsmedia\/' + song.album.album_art+')'});
            $('#mini_image').animate({marginTop:'0px'});
     $("#ilSong").html('<b>'+song.song+'</b>');
      var art = [];
      for(i=0;i<song.artists.length && i<5; i++) art.push(song.artists[i].artist);
      $("#ilArtist").html('- '+art.join(' ,'));
        song_playing = id;
        Jukebox.play_url('song_'+id,'http://192.168.121.5/songs/english/'+song.file_name);
    clearTimeout(interval);
    interval = setTimeout(function(){ count_increase(id); },60000);
    });
  }
}


function check_hash( name )
{
  hash = document.location.href.split('#')[1];
  if(!hash) hash="";
  hash = hash.replace(/\/$/, '');
  if(!prev_hash) prev_hash="";
  console.log('prev    '+prev_hash);
  console.log('hash    '+hash);
  prev_hash = prev_hash.replace(/\/$/, '');
  hash = hash.split('/');
  phash = prev_hash.split('/');
  if(name=='playing')
  {

    hsong = hash.indexOf('song')+1;
    psong = phash.indexOf('song')+1;
        if(hash[hsong]!=phash[psong] ) return false;
      return true;
  }
  if(name=='song')
  {
    if(hash.length == phash.length)
    {
      for(i=0;i<hash.length-1;i++)
        if(hash[i]!=phash[i] ) return false;
      return true;
    }
  return false;
  }
  else if(name=='artists' || name=='albums' || name=='playlists' || name=='search')
  {
     if(hash[0]==phash[0]) return true;
  }
  else
  {
    if(hash.length == phash.length)
    {
      for(i=0;i<1;i++)
        if(hash[i]!=phash[i] ) return false;
      return true;
    }
  return false;
  }
}


function split_hash(){
  hash = document.location.href.split('#')[1];
  if(!hash) hash="";
  hash = hash.replace(/\/$/, '');
  hash = hash.split('/');
  name = hash[0];
  song = hash.indexOf('song');
  if(song>=0 && check_hash('song') && !check_hash('playing')){ play(hash[song+1]); prev_hash=document.location.href.split('#')[1]; console.log(hash[song+1]); return;}
  if ( Object.keys(names).indexOf(name) >= 0){
            if(!check_hash(name))
            {
               $('#navigation').find('a').each(function(){
                if($(this).hasClass('selected')){
                  
                  // console.log($(this));
                  // $(this).find('div:nth-child(1)').css({'color':'#9C9C9C'});
                  $('#artists_icon').css({'color':'#9C9C9C'});
                  $('#trending_icon').css({'color':'#9C9C9C'});
                  $('#albums_icon').css({'color':'#9C9C9C'});
                  $('#home_icon').css({'color':'#9C9C9C'});
                  $('#shared_icon').css({'color':'#9C9C9C'});
                  $(this).removeClass('selected');
                  }
                  });
               $('#playlist_navigation').find('a').each(function(){
                if($(this).hasClass('selected')){
                  
                  // $(this).find('div:nth-child(1)').css({'color':'#9C9C9C'});
                  $('#artists_icon').css({'color':'#9C9C9C'});
                  $('#trending_icon').css({'color':'#9C9C9C'});
                  $('#albums_icon').css({'color':'#9C9C9C'});
                  $('#home_icon').css({'color':'#9C9C9C'});
                  $('#shared_icon').css({'color':'#9C9C9C'});
                  $(this).removeClass('selected');
                }
                  });
             $('#'+name+'_link').addClass('selected');
             $('#'+name+'_link>div:nth-child(1)').css({'color':'#ff5d42'});
            }
    if(hash.length == 2 || hash.length == 4){
      if(name == 'artists'){ if(!check_hash('artists')) display('artists'); display_artist(hash[1]); }
      if(name == 'albums'){ if(!check_hash('albums')) display('albums');  display_album(hash[1]); }
    }
    else{
      display(name);
    }
  }
  if( name == 'playlists' )
  { 
    $('#navigation').find('a').each(function(){
                if($(this).hasClass('selected')){
                  $(this).removeClass('selected');
                  // $(this).find('div:nth-child(1)').css({'color':'#9C9C9C'});
                  $('#artists_icon').css({'color':'#9C9C9C'});
                  $('#trending_icon').css({'color':'#9C9C9C'});
                  $('#albums_icon').css({'color':'#9C9C9C'});
                  $('#home_icon').css({'color':'#9C9C9C'});
                  $('#shared_icon').css({'color':'#9C9C9C'});
                }
                  });
    $('#playlist_navigation').find('a').each(function(){
                if($(this).hasClass('selected')){
                  $(this).removeClass('selected');
                  // $(this).find('div:nth-child(1)').css({'color':'#9C9C9C'});
                  $('#artists_icon').css({'color':'#9C9C9C'});
                  $('#trending_icon').css({'color':'#9C9C9C'});
                  $('#albums_icon').css({'color':'#9C9C9C'});
                  $('#home_icon').css({'color':'#9C9C9C'});
                  $('#shared_icon').css({'color':'#9C9C9C'});
                }
                  });

    $("#playlists_link").addClass('selected');
    $("#playlists_link>div:nth-child(1)").css({'color':'#ff5d42'});
    if(hash.length == 2 || hash.length == 4)
    {
    if(!check_hash('playlists')) display_playlists();
    display_playlist(Number(hash[1]));
      // console.log('sasasasa');
    }
    else
    {
      display_playlists();
    }
  }
  if( name == 'shared' )
  { 

     $('#navigation').find('a').each(function(){
                if($(this).hasClass('selected')){
                  $(this).removeClass('selected');
                  // $(this).find('div:nth-child(1)').css({'color':'#9C9C9C'});
                  $('#artists_icon').css({'color':'#9C9C9C'});
                  $('#trending_icon').css({'color':'#9C9C9C'});
                  $('#albums_icon').css({'color':'#9C9C9C'});
                  $('#home_icon').css({'color':'#9C9C9C'});
                  $('#shared_icon').css({'color':'#9C9C9C'});
                }
                  });
    $('#playlist_navigation').find('a').each(function(){
                if($(this).hasClass('selected')){
                  $(this).removeClass('selected');
                  // $(this).find('div:nth-child(1)').css({'color':'#9C9C9C'});
                  $('#artists_icon').css({'color':'#9C9C9C'});
                  $('#trending_icon').css({'color':'#9C9C9C'});
                  $('#albums_icon').css({'color':'#9C9C9C'});
                  $('#home_icon').css({'color':'#9C9C9C'});
                  $('#shared_icon').css({'color':'#9C9C9C'});
                  }
                });

    $("#shared_link").addClass('selected');
    $("#shared_link>div:nth-child(1)").css({'color':'#ff5d42'});
    if(hash.length == 2 || hash.length == 4)
    {
      if(!check_hash('shared')) display_public_playlists();
        display_playlist(Number(hash[1]));
    }
    else
    {
      display_public_playlists();
    }
  }
  if( name== 'search'){
    //$('#searchButton').click();
    //alert('hash   '+hash[1]);
    if(hash.length==1 || hash.length==3 || (hash.length>1 && hash[1]=='') )
    {
      console.log('sasa');
            $('#searchList').html($('#itemsDisplay').clone());
      $("#itemDisplay").hide();
    }
    else
    {
      if(!check_hash('search'))
        get_search_html(hash[1]);
      else
        search_full(hash[1]);
    }
  }
  if (song >= 0 && !check_hash('playing')){
    play(hash[song+1]);
  }
//  if (name!='search') prev_hash = document.location.href.split('#')[1];
    prev_hash = document.location.href.split('#')[1];
}


$('#create_new_input').bind('keypress',function(e){
        if(e.which == 13)
        {
            var val = $(this).val();
            if(val=='') return;
            create_playlist_queue(val);
            $(this).val('');
            $('#save_as_playlist_cancel').click();
        }
    });

$('#add_new_submit').on('click',function(e){
            var val = $('#create_new_input').val();
            if(val=='') return;
            create_playlist_queue(val);
            $('#create_new_input').val('');
            $('#save_as_playlist_cancel').click();
    });

$('#as_prev_submit').on('click',function(e){
            var val = $('#select_saved_playlist').find('option:selected').val();
            if(val=='0' || isNaN(val)) return;
            overwrite_playlist(val);
            $('#create_new_input').val('');
            $('#save_as_playlist_cancel').click();
            reload();
    });


$('#add_to_playlist_submit').on('click',function(e){
            var val = $('#add_to_saved_playlist').find('option:selected').val();
            if(val=='0' || isNaN(val)) return;
            if(adding_to_play) add_to_playlist(add_to_play,val);
            else add_to_playlist(queue,val);
            $('#add_to_playlist_cancel').click();
            reload();
            adding_to_play=false;
            add_to_play = [];
    });


function create_playlist_queue(val)
{
  var que = [];
  for(var i in queue)
  {
    if(que.indexOf(queue[i])>=0) continue;
    que.push(queue[i]);
  }
  que = que.join('b');
  console.log(que);
  $.post('playlists/',{name:val,songs:que});
  get_json('playlists');
}


function add_to_playlist(val,inc)
{

  var que = val.join('b');
  $.post('playlists_add/',{id:inc,songs:que});
}

function overwrite_playlist(inc)
{
  var que = [];
  for(var i in queue)
  {
    if(que.indexOf(queue[i])>=0) continue;
    que.push(queue[i]);
  }
  que = que.join('b');
  $.post('playlists_over/',{id:inc,songs:que});
}


function add_songs_url()
{
   if(trending_open){
     for(var i=0;i<trending_json.length;i++){
       songs_url[trending_json[i].id]=trending_json[i];
     }
   }
/*   if(artists_open)
     localStorage.setItem('artists_json', JSON.stringify(artists_json));
   if(albums_open)
     localStorage.setItem('albums_json', JSON.stringify(albums_json));
*/
}


function get_json(name)
{
        if (name in names) var show = names[name];
        else if(name=='playlists') var show=['playlists/'];
        else if(name=='public_playlists') var show=['playlists_public/'];
        var url = show[0];
        $.ajax(url,contentType= "application/json").done( function(data){
          if(name=='trending'){ 
            trending_json=data; trending_open=true; get_json('playlists');  }
          else if(name=='albums'){ 

            albums_json=data; albums_open=true; get_json('playlists'); }
          else if(name=='artists'){ 

            artists_json=data; artists_open=true; get_json('playlists'); }
          else if(name=='playlists'){ 

            playlists_json=data; playlists_open=true;  add_songs_url(); get_json('public_playlists'); }
          else if(name=='public_playlists'){  
            // loading = false;
            $('body').css({'opacity':'1'});
            $('#loading_div_spinner').css({'display':'none'});
            public_playlists_json=data; public_playlists_open=true;  add_songs_url();  }
          console.log(name);
        });
}

$( document ).ready(function() {
   
  });

//window.onhashchange = split_hash(); // For IE<8 and safari
$(window).on('hashchange', function() {split_hash();});


function options_binder()
{

$('.last').bind('click',function(){

      var id = $(this).attr('id').split('_')[1];
      if (id in songs_url) add_LS_queue(songs_url[id]);
      else
         $.ajax('song/'+id,contentType= "application/json").done( function(data){
             songs_url[id]=data;
             add_LS_queue(songs_url[id]);
           });
    });

$('.next').bind('click',function(){
      var id = $(this).attr('id').split('_')[1];
      if (id in songs_url) add_next_queue(songs_url[id]);
      else
         $.ajax('song/'+id,contentType= "application/json").done( function(data){
             songs_url[id]=data;
             add_next_queue(songs_url[id]);
           });
    });

$('.options_add_to_playlist').bind('click',function(){
      var id = $(this).attr('id').split('_')[1];
      add_to_play = [Number(id)];
      adding_to_play=true;
      $('#add_to_playlist').click();
    });

$('.delete_from_playlist').bind('click', function(){
      var index = $(this).attr('id').split('_')[1];
      var play_id = $(this).attr('id').split('_')[2];
      $(this).parents().eq(3).remove();
      delete_from_playlist(index,play_id);
    });
$('.share_url').bind('click', function(){
      var song_id = $(this).attr('id').split('_')[1];
     // copy_to_clipboard(song_id,this);
     /* var idd = '#'+$(this).attr("id");
    $(idd).zclip({
        path:STATIC_URL+'swf/jukebox/ZeroClipboard.swf',
        copy: function() { return window.location.href.split('#')[0]+"#trending/song/"+song_id },
       });
      console.log(idd);*/
    });
}

function language_binder()
{
 artist_language_dialog_binder(); 
 search_icon_input_binder();
}

function playlist_options_binder()
{

    $("#playlist_options").bind('change', function(){
            var val = $(this).val();
             if(val=="add_to_queue")
             {
                add_queue_playlist();
             }
             else if(val.split('_')[0]=="delete")
             {
                delete_playlist(val.split('_')[1]);
             }
             else if(val.split('_')[0]=="rename")
             {
                rename_playlist('mainbody', val.split('_')[1]);
             }
             else if(val.split('_')[0]=="publicToggle")
             {
                private_toggle_playlist(val.split('_')[1]);
                var tog_text = $("#public_toggle").text();
                if(tog_text=="Make Private") tog_text="Make Public";
                else tog_text="Make Private";
                $("#public_toggle").text(tog_text);
             }

             $("#playlist_options").val("default");

        });

}





$("#trending_link").click(function(){ hash_change("trending"); });  // changes hash when trending is clicked
$("#artists_link").click(function(){ hash_change("artists"); });    // changes hash when Artist is clicked
$("#albums_link").click(function(){ hash_change("albums"); });      // changes hash when Albums is clicked
$("#playlists_link").click(function(){ hash_change("playlists"); });      // changes hash when Albums is clicked
$("#shared_link").click(function(){ hash_change("shared"); });      // changes hash when Albums is clicked

function artist_ready(){
  $(".artist").on('click',function(){
      id = $(this).attr('id').split('_')[1];
      hash_change('artists',id);
         });
}
function album_ready(){
  $(".album").bind('click',function(){
      id = $(this).attr('id').split('_')[1];
      hash_change('albums',id);
    });
  $("#dynamicSearch").unbind('keyup').unbind('focus').unbind('blur');
  $('#dynamicSearch').bind('focus', function(){select=true;}).bind('keyup', function(e)
      {   if(e.keyCode == 27){
            $(this).toggle();
          }
          if ($("#dynamicSearch").val()==""){ $('#contentList').find('.start').show(); $("#contentList").find('li.album').show(); return; }
          var arr = eval("albums_json."+$('#artist_language>li.artist_language_selected').html());
          var fuse = new Fuse(arr,{ keys: ['album']});
          var results = fuse.search($('#dynamicSearch').val());
          $('#contentList').find('li.album').hide();
          for(var i in results)
          {
            $('#album_'+results[i].id).show();

          }
          var divs = $('#contentList').find('.start');
          for(var i=0;i<26;i++)
          {
            if ($(divs[i]).find('li.album:visible').length <= 0) $(divs[i]).hide();
          }

      }).bind('blur', function(){ select=false; });
}

function playlist_ready(){
  $(".playlist").on('click',function(){
      id = $(this).attr('id').split('_')[1];
      hash_change('playlists',id);
    });
  $(".shared").on('click',function(){
      id = $(this).attr('id').split('_')[1];
      hash_change('shared',id);
    });
}

function trending_ready(){
    
    $('.play_icon').bind('click',function(){
       var so = 'song_'+song_playing;
        if( $(this).parent().attr('id') == so){
             $('#bLeftPlay img').click();
          } 
    });
}


function song_ready()
{
  $(".song").bind('click',function(){
       song_bind($(this));
      });

      song_options_binder();
  

}

function search_ready()
{
  $(".searchItem").bind('click', function(){ closeSearch(); });
}

function closeSearch()
{
    $('#searchBig').select();
    $('#searchButton').addClass("notOpen");
     $("#bigwrapper").removeClass("blur_back");
    $("#searchDivcss").removeClass("searchLightboxOpen").addClass("searchLightboxClose");
     type=0;
//:# key_ready();

}

function song_bind(element){
 //   if(check_hash('song')){
   //   add_queue(element)}
      in_queue = element.hasClass('qitem');
      if(in_queue)
      {
       $('#queue_content').find('div').each(function(){
        if($(this).hasClass('qselected'))
          $(this).removeClass('qselected');
          });
        element.addClass('qselected');
      }
      id = element.attr('id').split('_')[1];
      if(Number(id) == song_playing)
      {
        play(song_playing);
      }
      hash = document.location.href.split('#')[1];
      hash = hash.split('/');
      if((i=hash.indexOf('song')) >=0 ){
        hash[i+1] = id;
        window.hash_change.apply(window, hash);
      }
      else{
        hash.push('song');
        hash.push(id);
        window.hash_change.apply(window, hash);
      }
}

function song_options_binder(){
/* settings add to playqueue etc */
var song_option_state = false;
$(".song_options").on('click',function(){
    $(".song_setting_box").css('display','block');
    });

/*$(".setting_button").mouseleave(function(){
    $(".song_setting_box").css('display','none');
    });
*/
$('.song_setting_box').mouseleave(function(){
    $(".song_setting_box").css('display','none');
    });

}

function playlist_song_options_binder(id, owner){
  
  if(owner===true){
  var oldIndex;
  $( "#play_sortable" ).sortable({
        start: function(e, ui) {
            oldIndex = ui.item.index();
            },
        update: function(e, ui) {
           var newIndex = ui.item.index();
          console.log(oldIndex +'    '+newIndex);
          change_index_playlist(oldIndex,newIndex,id);
        } 
        });
  $( "#play_sortable" ).sortable( "option", "containment", "parent" );
  }
  $( "#play_sortable" ).disableSelection();
  var playlist_setting_state=false;
  /* playlist list items setting */
  $('.iDoptions').on('click',function(){
      if(playlist_setting_state){
      $(this).find('.playlist_item_setting_box').css('display','none');
      playlist_setting_state=false;
      }
      else{
      $(this).find('.playlist_item_setting_box').css('display','block');
      playlist_setting_state=true;
      }
      });
  $('.playlist_item_setting_box').on('mouseleave',function(){ 
      $(this).css('display','none');
      playlist_setting_state=false;
      });

}

function search_icon_input_binder(){
      $('#searchIconTop>i').bind('click',function(){
          $("#dynamicSearch").toggle();
      });
}

function artist_language_dialog_binder(){

  $('#artist_language>li').bind('click',function(){


         var language_selected = $(this).html();
         $('#artist_language>li').removeClass();
         $(this).addClass('artist_language_selected');
          // console.log(language_selected);
          $('#contentList').empty();
          // console.log(albums_json[language_selected]);
          for (var i=0; i<albums_json[language_selected].length; i++){
          get_album_html(albums_json[language_selected][i]);
          }
      album_ready();
      song_ready();
  });
  // $('#artist_language').bind('change', function(e){
  //         var language_selected = $(this).val();
  //         $('#contentList').empty();
  //       for (var i=0; i<albums_json[language_selected].length; i++){
  //         get_album_html(albums_json[language_selected][i]);
  //           }
  //     album_ready();
  //     song_ready();
  //     });
}

function albums_song_options_binder(){
    
  var album_setting_state=false;
  /* album list items setting */
  $('.album_options').on('click',function(e){
      e.stopPropagation();
      if(album_setting_state){
      $(this).find('.album_item_setting_box').css('display','none');
      album_setting_state=false;
      }
      else{
      $(this).find('.album_item_setting_box').css('display','block');
      album_setting_state=true;
      }
      });
  $('.album_item_setting_box').on('mouseleave',function(){ 
      $(this).css('display','none');
      album_setting_state=false;
      });

}
function artist_song_options_binder(){
    
  var artist_setting_state=false;
  /* album list items setting */
  $('.artist_options').on('click',function(e){
      e.stopPropagation();
      if(artist_setting_state){
      $(this).find('.artist_item_setting_box').css('display','none');
      artist_setting_state=false;
      }
      else{
      $(this).find('.artist_item_setting_box').css('display','block');
      artist_setting_state=true;
      }
      });
  $('.artist_item_setting_box').on('mouseleave',function(){ 
      $(this).css('display','none');
      artist_setting_state=false;
      });

}


function queue_binder()
{
  $('.queue_item_remove').bind('click',function(){
          var elm = $(this).parent();
          if (elm.hasClass('qselected')) return;
          var cnt=0;
          var elm = this;
          $('#queue_content').children().each(function(){
              if($(this).children()[0]==elm)
              {
                $(this).remove();
                remove_from_queue(cnt);
                return;
              }
              cnt++;
            });

      });
}

var albums_json1 = {};
var artists_json1 = {};
var songs_json1 = {};
var artists_by_name = {};
var albums_by_name = {};
var songs_by_name = {};
var artists_name = [];
var albums_name = {};
var songs_name = [];

$(document).ready(function(){
    var que = localStorage.getItem('queue');
   if(que != null && que.length>0)
    {
      $.get('queue/',{qu:que},function(data){
          var qu = data['queue'];
          que = que.split(',');
          for(var i=0;i<que.length;i++)
          {
            add_LS_queue(qu[que[i]]);
          }
        });
        
    }
    key_ready();
    login();
    
    $('#seeMore').on('click',function(){
          var search_str = $('#searchBig').val();
          hash_change('search',search_str);
          closeSearch();
      });
   // loading line starts here 
   $.getJSON('/songsmedia/songs_json/all_artists.json', function(data){
         // loading line loading ends
         artists_json1 = data;
         for(var i in artists_json1){ artists_by_name[artists_json1[i].artist] = artists_json1[i]; artists_name.push(artists_json1[i].artist); }
         artists_name.sort();
        artists_open=true;
         albums_by_name['Hindi'] = {};
         albums_name['Hindi'] = [];
         albums_by_name['English'] = {};
         albums_name['English'] = [];
         for(var i in artists_json1){ for(var j = 0; j< artists_json1[i].album_set.length; j++ ){ if(albums_name['Hindi'].indexOf(artists_json1[i].album_set[j].album ) >= 0  ||  artists_json1[i].artist!="Hindi") continue; albums_by_name['Hindi'][artists_json1[i].album_set[j].album] =  albums_json1[artists_json1[i].album_set[j].id] = artists_json1[i].album_set[j]; albums_name['Hindi'].push(artists_json1[i].album_set[j].album); }}
         for(var i in artists_json1){ for(var j = 0; j< artists_json1[i].album_set.length; j++ ){ if(albums_name['English'].indexOf(artists_json1[i].album_set[j].album ) >= 0  ||  artists_json1[i].artist=="Hindi") continue; albums_by_name['English'][artists_json1[i].album_set[j].album] =  albums_json1[artists_json1[i].album_set[j].id] = artists_json1[i].album_set[j]; albums_name['English'].push(artists_json1[i].album_set[j].album); }}
        albums_name['Hindi'].sort();
        albums_name['English'].sort();
        albums_open=true;
   split_hash();
    
  hash = document.location.href.split('#')[1];
  if(!hash)
  {
    hash_change('trending');
  }
// loading
//loading=true;
$('body').css({'opacity':'0.4'});
$('#loading_div_spinner').css({'display':'block'});
   get_json('trending');
 //  clip = new ZeroClipboard.Client();

/*        for(var i in artists_json1){ for(var j = 0; j< artists_json1[i].album_set.length; j++ ){ if(songs_name.indexOf(artists_json1[i].album_set[j].album ) >= 0) continue; for(var k=0; k<artists_json1[i].album_set[j].song_set.length ; k++){ songs_by_name[artists_json1[i].album_set[j].song_set[k].song] = songs_json1[artists_json1[i].album_set[j].song_set[k].id] = artists_json1[i].album_set[j].song_set[k]; songs_name.push(artists_json1[i].album_set[j].song_set[k].song); } }} */
       });
});

function reload()
{
  $.ajax('playlists/',contentType= "application/json").done( function(data){
          playlists_json=data; 
          playlists_open=true;  
          add_songs_url();
  hash = document.location.href.split('#')[1];
  if(!hash) hash="";
  hash = hash.replace(/\/$/, '');
  hash = hash.split('/');
  name = hash[0];
  
  if( name == 'playlists' )
  {
    if(hash.length == 2 || hash.length == 4)
    {
     display_playlists();
    display_playlist(Number(hash[1]));
    }
    else
    {
        display_playlists();
    }
  }
  else if( name == 'shared' )
  {
    if(hash.length == 2 || hash.length == 4)
    {
     display_public_playlists();
    display_playlist(Number(hash[1]));
    }
    else
    {
        display_public_playlists();
    }
  }
  });
}

function login()
{

  $(document).on("login", function(){
          if(login_cancel){ login_cancel=false; return;}
              reload();
           logged_in=true;
           $("#signin_button").text('Sign Out');
           login_cancel=false;

     });
  $("#signin_button_large").on('click', function(){
          if(!logged_in)
          {
            var uid = $('#jb_username').val();
            var pwd = $('#jb_password').val();
            $.post('/login/',{username:uid, password:pwd}, function(data){
              reload();
                    $("#signin_button").text('Sign Out');
                    logged_in = true;
                    $('#signin_cancel').click();
                    $('#jb_username').val('');
                    $('#jb_password').val('');
              });

          }

      });
  $("#signin_button").on('click', function(){
            if(logged_in)
            $.get('/logout/', function(){
              reload();
           //     get_json('playlists');
                $("#signin_button").text('Sign In');
                logged_in = false;
              });
            });
}



/*function copy_to_clipboard(song_id,elm)
{
  var copy_text = document.location.href.split('#')[0] + '#trending/song/'+song_id;
  clip.setText(copy_text);
  clip.glue(elm);
  alert('copied '+copy_text);
}
*/
function display_public_playlists(){
      $("#centerdata").empty();
        $("#centerdata").append('<div id="playlistsList">  <div class="nano" id="left_playlist_list">  <div id="contentList" class="content"> </div></div></div>');
  if( public_playlists_open )
  {
      var data = public_playlists_json;
        var html = '<div class="start"><div class="list_alpha"><div class="playlist_create" id="playlist_new"><div id="plus_icon"><i class="icon-plus"></i></div><div id="create_new_div"><a id="create_new">Create New</a></div></div> <ul id= "playlists"></ul></div></div>';
      $("#contentList").append(html);
      for(var i=0; i<data.length; i++){
        var playlist = data[i];
        $("#playlists").append('<li class="shared" id="shared_'+ playlist.id +'"><span>'+playlist.name+'</span></li>');
      }
          $("#playlistsList").append('<div id="playlist_view"></div>');
          // $("#playlistsList").append('<div id="playlist_panel_hide"><i class="icon-reorder"></i></div>');
          lPlaylists();
      playlist_ready();
    }
  else{
  url = 'playlists_public/';
  $.ajax(url,{ type:"GET" } ,contentType= "application/json").done( function(data){
      $("#centerdata").empty();
        $("#centerdata").append('<div id="playlistsList">  <div class="nano" id="left_playlist_list">  <div id="contentList" class="content"> </div></div></div>');
        html = '<div class="start"><div class="list_alpha"><div class="playlist_create" id="playlist_new"><div id="plus_icon"><i class="icon-plus"></i></div><div id="create_new_div"><a id="create_new">Create New</a></div></div> <ul id= "playlists"></ul></div></div>';
      $("#contentList").append(html);
      for(var i=0; i<data.length; i++){
        var playlist = data[i];
        $("#playlists").append('<li class="shared" id="shared_'+ playlist.id +'"><span>'+playlist.name+'</span></li>');
      }
          $("#playlistsList").append('<div id="playlist_view"></div>');
          // $("#playlistsList").append('<div id="playlist_panel_hide"><i class="icon-reorder"></i></div>');
          lPlaylists();
      playlist_ready();
      public_playlists_json=data;
      public_playlists_open=true;
    });
    }
}




