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



function search_full(search_str){
$('#inputFor').val(search_str);
    $.get('search_all/',{q:search_str}, function(data){
            var songs = data.songs;
            var albums = data.albums;
            var artists = data.artists;
            $('#search_song_count').html('Songs('+songs.length+')');
            $('#song_searchList').html($('#itemsDisplay').clone());
           // $('#centerdata').append('<div id="searchItemToShow"><span>Songs('+songs.length+')</span><span>Albums('+albums.length+')</span><span>Artists('+artists.length+')</span></div><div id="searchUnderline"></div></div>'+
       for(var i=0; i<songs.length;i++){
            $('#song_searchList').append(''+
		'		<li>'+
		'			<div class="iDsrno">'+left_add_zero(i+1)+'</div>'+
		'			<div class="iDname song draggable" id="song_'+songs[i].id+'">'+songs[i].song+'</div>'+
		'			<div class="iDalbum album" id="album_'+songs[i].album.id+'">'+songs[i].album.album+'</div>'+
		'			<div class="iDartist artist" id="artist_'+songs[i].artists[0].id+'">'+songs[i].artists[0].artist+'</div>'+
		'		</li>');
        if(!(songs[i].id in songs_url)) songs_url[songs[i].id]=songs[i];
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
            $('#searchViewOpened').append('<div id="searchItemToShow"><span id="search_song_count">Songs(0)</span><span id="search_album_count">Albums(0)</span><span id="search_artist_count">Artists(0)</span></div><div id="searchUnderline"></div></div>'+
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
		'			<div class="iDalbum">ALBUM</div>'+
		'			<div class="iDartist">ARTIST</div>'+
		'		</li>'+
    '</ul>'+
    '<ul class="searchList" id="artist_searchList">'+
		'		<li id="itemsDisplay">'+
		'			<div class="iDsrno" style="visibility:hidden;font-size: 12px;">99</div>'+
		'			<div class="iDname">NAME</div>'+
		'			<div class="iDalbum">ALBUM</div>'+
		'			<div class="iDartist">ARTIST</div>'+
		'		</li>'+
    '</ul>'+
    '</div>'
    );
search_full(search_str);
$('#inputFor').on("keyup", function (event) {
    q = $(this).val();
    hash_change('search',q);
    console.log('heree');
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
var trending_open=false;
var now_display='trending';
var albums_json = {};
var artists_json = {};
var playlists_json = {};
var trending_json={};
var queue = [];
var in_queue=false;
var songs_url = {};
var song_playing=0;
var login_cancel=false;


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
        $("#songSearch").empty();
        $("#albumSearch").empty();
        $("#artistSearch").empty();
        return;
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
       $("#songSearch").append('<div class="searchHeading">SONGS<span> ('+data.songs.length+')</span></div>');
       $("#songSearch").append('<div> <ul  id="songSearchSpan" class="searchResultList" > </ul> </div>');
       for(var i=0; i<data.songs.length; i++)
       {
         var html = '<li class="song" id="song_'+data.songs[i].id+'"><div class="searchItemImg" style="background-image:url('+'http://192.168.121.5\/songsmedia\/' + data.songs[i].album.album_art+')" ></div>'
                  +  '<div class="searchItemDetails">'
		              +   '<div class="itemName">'+ data.songs[i].song+'</div>'
		              +    '<div class="itemSubDetail">'+data.songs[i].artists[0].artist+'</div></div></li>';
         $("#songSearchSpan").append(html);
         songs_url[data.songs[i].id]=data.songs[i];
       }
       $("#albumSearch").empty();
       $("#albumSearch").append('<div class="searchHeading">Albums<span> ('+data.albums.length+')</span></div>');
       $("#albumSearch").append('<div> <ul  id="albumSearchSpan" class="searchResultList" > </ul> </div>');
       for(var i=0; i<data.albums.length; i++)
       {
         var html = '<li class="album searchItem" id="album_'+data.albums[i].id+'"><div class="searchItemImg" style="background-image:url('+'http://192.168.121.5\/songsmedia\/' + data.albums[i].album_art+')" ></div>'
                  +  '<div class="searchItemDetails">'
		              +   '<div class="itemName">'+ data.albums[i].album+'</div>'
		              +    '<div class="itemSubDetail">'+data.albums[i].artists[0].artist+'</div></div></li>';
         $("#albumSearchSpan").append(html);
       }
       $("#artistSearch").empty();
       $("#artistSearch").append('<div class="searchHeading">Artists<span> ('+data.artists.length+')</span></div>');
       $("#artistSearch").append('<div> <ul  id="artistSearchSpan" class="searchResultList" > </ul> </div>');
       for(var i=0; i<data.artists.length; i++)
       {
         var html = '<li class="artist searchItem" id="artist_'+data.artists[i].id+'"><div class="searchItemImg" style="background-image:url('+'http://192.168.121.5\/songsmedia\/' + data.artists[i].artist_art+')" ></div>'
                  +  '<div class="searchItemDetails">'
		              +   '<div class="itemName">'+ data.artists[i].artist+'</div>'
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
        items = albums_json; 
        $("#centerdata").append('<div id="albumsList">  <div class="nano" id="left_album_list">  <div id="contentList" class="content"> </div></div></div>');
        for (var i=0; i<items.length; i++){
          get_album_html(items[i]);
        }
        $("#albumsList").append('<div id="oneAlbumOpened"><div id="oaoWrapper"></div></div>');
        $("#oneAlbumOpened").append('<div id="album_panel_hide"><i class="icon-reorder"></i></div>');
        lAlbums();
        album_ready();
        return;
    }
    if(artists_open && name=='artists')
    {
      $("#centerdata").empty();
        items = artists_json; 
        $("#centerdata").append('<div id="artistsList">  <div class="nano" id="left_album_list">  <div id="contentList" class="content"> </div></div></div>');
        for (var i=0; i<items.length; i++){
          get_artist_html(items[i]);
        }
        $("#artistsList").append('<div id="artist_view"></div>');
        $("#artistsList").append('<div id="artist_panel_hide"><i class="icon-reorder"></i></div>');
        lArtists();
        artist_ready();
       
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
        $("#centerdata").append('<div id="albumsList">  <div class="nano" id="left_album_list">  <div id="contentList" class="content"> </div></div></div>');
      }
      if(name=='artists')
      {
        $("#centerdata").append('<div id="artistsList">  <div class="nano" id="left_album_list">  <div id="contentList" class="content"><div id="artist_language"><div id="artist_language_dropdown" style="display:none"><ul><li>Hindi</li><li>Punjabi</li><li>Tamil</li><li>Telugu</li></ul></div><span id="artist_language_display">English</span><span id="artist_language_icon"><i class="icon-sort-down"></i></span></div></div></div></div>');
      }
      items=data;
      for (var i=0; i<items.length; i++){
	      if(name=='trending')
	      {
		$("#container").append(func(items[i]));
	      }
        else if(name=='albums' || name=='artists')
	      {
		func(items[i]);
	      }
              else
        $("#centerdata").append(func(items[i]));
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
        $("#oneAlbumOpened").append('<div id="album_panel_hide"><i class="icon-reorder"></i></div>');
        lAlbums();
        albums_json = items;
        albums_open = true;
      }
      if(name=='artists')
      {
       // $("#centerdata").append('</div></div></div>');
        $("#artistsList").append('<div id="artist_view"></div>');
        $("#artistsList").append('<div id="artist_panel_hide"><i class="icon-reorder"></i></div>');
        lArtists();
        artists_json = items;
        artists_open = true;
      }
    });
  }
}


// display_album for displaying a specific album
function display_album(id){
  url = "albums/" + id;
    $.ajax(url,contentType= "application/json").done( function(data){
      var album = data;
      $("#oaoWrapper").empty();
      $("#oaoWrapper").append('<div id="oaoLeft"></div>    <div id="oaoRight"> <div id="popular_list"></div> </div>');
      $("#oaoLeft").append('<img class="album draggable" src="http://192.168.121.5/songsmedia/'+ album.album_art +'"  style="display:block; width:300px; height:300px;"></img>');  // change the css accordingly
      $("#oaoLeft").append('<div id="oaoLInfo"> <div class="playable">'+album.album+'</div> </div>');
   //   html = "<br> Album Name: <br>" + album.album + "<br> Artists: ";
      for(var j=0; j<album.artists.length && j<10 ; j++)
      {
        var k = album.artists[j].id
        $('#oaoLInfo').append("<div class='artist' id='artist_"+k+"'>" + album.artists[j].artist + "</div> ");
      }
      //  html += "<br> <img src='/media/"+ album.album_art + "' width='300px' height='300px'> <br> <br> Songs: <br>";
      html = '<ul>';
      for(var j=0; j<album.song_set.length; j++)
      {
         var k = album.song_set[j].id;
       // html += "" + album.song_set[j].song + "<br> ";
        html += '<li class="popular_item song draggable" id="song_'+k+'"><div id="list_number">'+left_add_zero(j+1)+'</div>  <div id="p_song_name">'+album.song_set[j].song +'</div><div class="album_options"><i class="album_options_button icon-ellipsis-horizontal"></i><div class="album_item_setting_box"><ul><li class="song" id="song_'+k+'">Play now</li><li class="next" id="next_'+k+'">Play next</li><li class="last" id="last_'+k+'">Play last</li><li class="options_add_to_playlist" id="add_'+k+'">Add to playlist</li><li class="share_url" id="share_'+k+'">Share</li></ul></div></div>';
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
      {
        html = '<div class="artist_album">'
                + '<div class="artist_album_pic album draggable"><img src="http://192.168.121.5/songsmedia/'+ artist.album_set[j].album_art +'"></img></div>'
                + '<div id="artist_song_list">'
                + '<div id="popular_heading"> '+artist.album_set[j].album+' </div>'
                + '<div id="popular_list">'
                + '<ul>';

      for(var k=0; k<artist.album_set[j].song_set.length; k++)
      {
        var l = artist.album_set[j].song_set[k].id;

       // html += "" + album.song_set[j].song + "<br> ";
        html += '<li class=" song popular_item draggable" id="song_'+l+'"><div id="list_number">'+left_add_zero(k+1)+'</div> <div id="p_song_name">'+ artist.album_set[j].song_set[k].song +'</div><div class="artist_options"><i class="artist_options_button icon-ellipsis-horizontal"></i><div class="artist_item_setting_box"><ul><li class="song" id="song_'+l+'">Play now</li><li class="next" id="next_'+l+'">Play next</li><li class="last" id="last_'+l+'">Play last</li><li class="options_add_to_playlist" id="add_'+l+'">Add to playlist</li><li class="share_url" id="share_'+l+'">Share</li></ul></div></div>';
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
      $('body').animate({scrollTop:0}, '500', 'swing', function() { 
     $(document).scroll(function () { 

       $('#artist_body').css({
         'top' : -($(this).scrollTop()/1.4)+"px"
         }); 

       $('#artistInfo').css({
         'top' : -($(this).scrollTop()/1.4)+301+"px"
         }); 
       $('#layer').css({
         'top' : -($(this).scrollTop()/1.4)+255+"px"
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
  //  return;
    }
    else
    {
      console.log(data.active+'asasas');
       
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
        html = '<div class="start"><div class="list_alpha"><div class="playlist" id="playlist_new"><div id="plus_icon"><i class="icon-plus"></i></div><div id="create_new_div"><a id="create_new">Create New</a></div></div> <ul id= "playlists"></ul></div></div>';
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
      var songs = playlist.songs.split('b');
      $("#playlist_view").empty();
      $("#playlist_view").append('<div id="playlistBanner"></div>');
  //    debugger;
      $("#playlistBanner").append('<div id="layerBanner" style="background:url(\'\/static/images/jukebox/gradientCover.png\'); " ></div>');
      $("#playlistBanner").append('<ul><li></li><li></li><li></li><li></li><li></li></ul>');
      $("#playlistBanner").append('<div id="playlistInfo"><div id="playlistName">'+playlist.name+'</div><div id="playlistSongCount">'+songs.length+' Songs</div></div>');
      $("#playlist_view").append('<div id="viewPlaylist"><div id="playlistContentFull"></div></div>');
      var html = '<ul id="play_sortable">';
      for(var j=0; j<songs.length; j++)
      {
        var k = playlist.songs_list[parseInt(songs[j])].id;
        var id = 'song_'+k;
        var image = 'http://192.168.121.5\/songsmedia\/' + playlist.songs_list[parseInt(songs[j])].album.album_art;
        image = 'http://192.168.121.5'+image;
        var artist_name = playlist.songs_list[parseInt(songs[j])].artists[0].artist;
        var album_name = playlist.songs_list[parseInt(songs[j])].album.album;
        var song_name = playlist.songs_list[parseInt(songs[j])].song;
        var artist_id = playlist.songs_list[parseInt(songs[j])].artists[0].id;
        var album_id = playlist.songs_list[parseInt(songs[j])].album.id;
        var file_name = playlist.songs_list[parseInt(songs[j])].file_name;
        //'<div class="pqimage" style="background:url(\''+image+'\'); background-size:cover">'
        html += '<li ><div class="iDsrno">'+left_add_zero(j+1)+'</div><div class="iDname song draggable" id="'+id+'">'+song_name+'</div><div class="iDalbum album" id="album_'+album_id+'">'+album_name+'</div><div class="iDartist artist" id="artist_'+artist_id+'">'+artist_name+'</div id="iDoptions"><div class="iDoptions"><i id="playlist_setting_icon" class="icon-ellipsis-horizontal"></i><div class="playlist_item_setting_box"><ul><li class="song" id="song_'+k+'">Play now</li><li class="next" id="next_'+k+'">Play next</li><li class="last" id="last_'+k+'">Play last</li><li class="options_add_to_playlist" id="add_'+k+'">Add to playlist</li><li class="share_url" id="share_'+k+'">Share</li><li class="delete_from_playlist" id="delete_'+j+'_'+play_id+'">Delete</li></ul></div></div></li>';
        if(!(playlist.songs_list[parseInt(songs[j])].id in songs_url)) songs_url[playlist.songs_list[parseInt(songs[j])].id]=playlist.songs_list[parseInt(songs[j])];
      }
      html +='</ul>';
      $('#playlistContentFull').append(html);

       var widthOfDiv = $('#playlist_view').width()/5;
       $('#playlistBanner ul li').css({width:widthOfDiv,height:widthOfDiv});
       $('#playlistBanner').css({height:widthOfDiv});
       $('#layerBanner').css({top:widthOfDiv-100+5});
        $("#playlistInfo").css({top:widthOfDiv-100+5+50});



      album_ready();
      artist_ready();
      song_ready();
      dragging();
      playlist_song_options_binder(play_id);
      options_binder();
    });
}


// for 1 song html
function get_song_html(song)
{
  var album=song.album;
  var album_art;
  if(album){ album_art = album.album_art; album= album.album; }
  else{ album=" "; album_art=" ";}
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
   for (var j=0; j<song.artists.length; j++)
   {
     html1 += song.artists[j].artist;
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
    Jukebox.play_url('song_'+id,'http://192.168.121.5/songs/english/'+song.file_name);
    if( !in_queue && (id != song_playing)){ add_queue_song(song); now_playing=queue.length-1; }
    $("#musicPlayerPic").empty();
    $("#mini_image").css({'background-image':'url('+'http://192.168.121.5\/songsmedia\/' + song.album.album_art+')'});
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
        $("#mini_image").css({'background-image':'url('+'http://192.168.121.5\/songsmedia\/' + song.album.album_art+')'});
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

    song = hash.indexOf('song');
    if(hash.length-song == phash.length-song)
    {
      for(i=song;i<hash.length;i++){ console.log(hash[i]+'  '+phash[i]);
        if(hash[i]!=phash[i] ) return false;}
      return true;
    }
  return false;
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
  if(song>=0 && check_hash('song')){ play(hash[song+1]); prev_hash=document.location.href.split('#')[1]; console.log(hash[song+1]); return;}
  if ( Object.keys(names).indexOf(name) >= 0){
            if(!check_hash(name))
            {
               $('#navigation').find('a').each(function(){
                if($(this).hasClass('selected'))
                  $(this).removeClass('selected');
                  });
             $('#'+name+'_link').addClass('selected');
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
    if(hash.length == 2 || hash.length == 4)
    {
    if(!check_hash('playlists')) display_playlists();
    display_playlist(Number(hash[1]));
      console.log('sasasasa');
    }
    else
    {
      display_playlists();
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
  if (song >= 0){
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
  var que = queue.join('b');
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
  var que = queue.join('b');
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
        var url = show[0];
        $.ajax(url,contentType= "application/json").done( function(data){
          if(name=='trending'){ trending_json=data; trending_open=true; get_json('albums');  }
          else if(name=='albums'){ albums_json=data; albums_open=true; get_json('artists'); }
          else if(name=='artists'){ artists_json=data; artists_open=true; get_json('playlists'); }
          else if(name=='playlists'){ playlists_json=data; playlists_open=true;  add_songs_url();  }
          console.log(name);
        });
}
$( document ).ready(function() {
   split_hash();
    
  hash = document.location.href.split('#')[1];
  if(!hash)
  {
    hash_change('trending');
  }

   get_json('trending');
 //  clip = new ZeroClipboard.Client();
   
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
    });
}





$("#trending_link").click(function(){ hash_change("trending"); });  // changes hash when trending is clicked
$("#artists_link").click(function(){ hash_change("artists"); });    // changes hash when Artist is clicked
$("#albums_link").click(function(){ hash_change("albums"); });      // changes hash when Albums is clicked
$("#playlists_link").click(function(){ hash_change("playlists"); });      // changes hash when Albums is clicked

function artist_ready(){
  $(".artist").on('click',function(){
      id = $(this).attr('id').split('_')[1];
      hash_change('artists',id);
         });
}

function album_ready(){
  $(".album").on('click',function(){
      id = $(this).attr('id').split('_')[1];
      hash_change('albums',id);
    });
}

function playlist_ready(){
  $(".playlist").on('click',function(){
      id = $(this).attr('id').split('_')[1];
      hash_change('playlists',id);
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

function playlist_song_options_binder(id){
  
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

function artist_language_dialog_binder(){
    var display_state = false;
  $('#artist_language').on('click',function(){
       if(display_state){
               
      $('#artist_language_dropdown').css('display','none');
      display_state=false;
         }
         else{
      $('#artist_language_dropdown').css('display','block');
      display_state=true;
      }
      }
      );

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
    
});

function reload()
{
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
}

function login()
{

  $(document).on("login", function(){
          if(login_cancel){ login_cancel=false; return;}
           console.log('asa');
           $.ajax('playlists/',contentType= "application/json").done( function(data){
              playlists_json=data;
              playlists_open=true;
              reload();
              });
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
           $.ajax('playlists/',contentType= "application/json").done( function(data){
              playlists_json=data;
              playlists_open=true;
              reload();
              });
           //         get_json('playlists');
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
           $.ajax('playlists/',contentType= "application/json").done( function(data){
              playlists_json=data;
              playlists_open=true;
              reload();
              });
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
