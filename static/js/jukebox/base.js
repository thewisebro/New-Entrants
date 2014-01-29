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
var album_open=false;
var artist_open=false;
var trending_open=false;
var now_display='trending';
var album_html = '';
var artist_html = '';
var trending_html='';





var song_playing;
/*$('form#playlist').on('submit', function(e) {
  $.ajax({
      type: 'post',
      url: 'playlist/',
      data: $(this).serialize(),
      success: function () {
        display_playlists($('#username').val());
       $('form#playlist').trigger('reset');
      }
      });
  e.preventDefault();
});
*/
/*

$('form#search').on('submit', function(e) {
    q = $(this).find("input").val();
    href = '#search/' + q;
    document.location.href = href;
  $.ajax({
      type: 'get',
      url: 'search/',
      data: $(this).serialize(),
      success: function (data) {
       $("#append").empty();
       $("#append").append("<br> Songs: <br>")
       for(var i=0; i<data.songs.length; i++)
       {
         $("#append").append(get_song_html(data.songs[i]))
       }
       $("#append").append("<br><hr><br> Albums: <br>")
       for(var i=0; i<data.albums.length; i++)
       {
         $("#append").append(get_album_html(data.albums[i]))
       }
       $("#append").append("<br><hr><br> Artists: <br>")
       for(var i=0; i<data.artists.length; i++)
       {
         $("#append").append(get_artist_html(data.artists[i]))
       }
       $('form#search').trigger('reset');
      artist_ready();
      album_ready();
      song_ready();
      }
      
      });
  e.preventDefault();
});
*/

$('#searchBig').bind("keyup", function (event) {
    q = $(this).val();
    hash_change('search',q);
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
         var html = '<li class="song" id="song_'+data.songs[i].id+'"><div class="searchItemImg" ></div>'
                  +  '<div class="searchItemDetails">'
		              +   '<div class="itemName">'+ data.songs[i].song+'</div>'
		              +    '<div class="itemSubDetail">'+data.songs[i].artists[0].artist+'</div></div></li>';
         $("#songSearchSpan").append(html);
       }
       $("#albumSearch").empty();
       $("#albumSearch").append('<div class="searchHeading">Albums<span> ('+data.albums.length+')</span></div>');
       $("#albumSearch").append('<div> <ul  id="albumSearchSpan" class="searchResultList" > </ul> </div>');
       for(var i=0; i<data.albums.length; i++)
       {
         var html = '<li class="album" id="album_'+data.albums[i].id+'"><div class="searchItemImg"></div>'
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
         var html = '<li class="artist" id="artist_'+data.artists[i].id+'"><div class="searchItemImg"></div>'
                  +  '<div class="searchItemDetails">'
		              +   '<div class="itemName">'+ data.artists[i].artist+'</div>'
		              +    '</div></li>';
         $("#artistSearchSpan").append(html);
       }
      artist_ready();
      album_ready();
      song_ready();
      hash = document.location.href.split('#')[1];
      if(!hash) hash="";
      hash = hash.split('/');
      if(hash[1]=='') 
      {
        $("#songSearch").empty();
        $("#albumSearch").empty();
        $("#artistSearch").empty();
      }
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
    if(name=='trending')
    {
      if(trending_open)
      {
        $('#centerdata').html(trending_html);
        lTrending();
        song_ready();
        return;
      }
     }
    if(name=='artists' || name=='albums')
    { 
      if(album_open && name=='albums')
      {
        $('#centerdata').html(album_html);
        lAlbums();
        album_ready();
        return;
      }
      if(artist_open && name=='artists')
      {
        $('#centerdata').html(artist_html);
        lArtists();
        artist_ready();
        return;
      }
     }
    // for hashtags
    var show = names[name];
    var url = show[0];
    var func = window[show[1]];
    var items=[];
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
        $("#centerdata").append('<div id="artistsList">  <div class="nano" id="left_album_list">  <div id="contentList" class="content"> </div></div></div>');
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
        trending_html = $("#centerdata").html();
        trending_open=true;
      }
      if(name=='albums')
      {
     //   console.log('yoooooooo');
       // $("#centerdata").append('</div></div></div>');
        $("#albumsList").append('<div id="oneAlbumOpened"><div id="oaoWrapper"></div></div>');
        $("#oneAlbumOpened").append('<div id="album_panel_hide"><i class="icon-reorder"></i></div>');
        lAlbums();
        album_html = $("#centerdata").html();
        album_open=true;
      }
      if(name=='artists')
      {
     //   console.log('yoooooooo');
       // $("#centerdata").append('</div></div></div>');
        $("#artistsList").append('<div id="artist_view"></div>');
        $("#artistsList").append('<div id="artist_panel_hide"><i class="icon-reorder"></i></div>');
        lArtists();
        artist_html = $("#centerdata").html();
        artist_open=true;
      }
    });
  }
}


// display_album for displaying a specific album
function display_album(id){
  url = "albums/" + id;
    $.ajax(url,contentType= "application/json").done( function(data){
      album = data[0];
      $("#oaoWrapper").empty();
      $("#oaoWrapper").append('<div id="oaoLeft"></div>    <div id="oaoRight"> <div id="popular_list"></div> </div>');
      $("#oaoLeft").append('<img src="/media/'+ album.album_art +'"  style="display:block; width:300px; height:300px;"></img>');  // change the css accordingly
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
       // html += "" + album.song_set[j].song + "<br> ";
        html += '<li class="popular_item song" id="song_'+album.song_set[j].id+'"> <div id="p_song_name">'+album.song_set[j].id_no+' ' +album.song_set[j].song +'</div>'
                +   ' <div class="miniIcons" id="p_alb_controls">'
                +       '<a href=""></a>' 
                +       '<a href=""></a>' 
                +       '<a href=""></a>' 
                +    '</li>';

      }
      $("#popular_list").append(html);

      artist_ready();
      song_ready();
    });

}



// display_artist for displaying a specific artist
function display_artist(id){
  url = "artists/" + id;
    $.ajax(url,contentType= "application/json").done( function(data){
      artist = data[0];
      $("#artist_view").empty();
      $("#artist_view").append('<div id="artist_banner" style="background:url('+'\'\/media\/' + artist.cover_pic +  '\'); background-size:cover; "></div>');
  //    debugger;
      $("#artist_banner").append('<div id="layer" style="background:url(\'\/static/images/jukebox/gradientCover.png\'); " ></div>');
    //  console.log('abcdddddddddddddddd');
      $("#artist_banner").append('<div id="artistInfo"><div id="artistName">'+artist.artist+'</div><div id="artistAlbumCount">'+artist.album_set.length+' Albums</div></div>');
      $("#artist_view").append('<div id="artist_body"></div>');
      for(var j=0; j<artist.album_set.length; j++)
      {
        html = '<div class="artist_album">'
                + '<div class="artist_album_pic"><img src="/media/'+ artist.album_set[j].album_art +'"></img></div>'
                + '<div id="artist_song_list">'
                + '<div id="popular_heading"> '+artist.album_set[j].album+' </div>'
                + '<div id="popular_list">'
                + '<ul>';

      for(var k=0; k<artist.album_set[j].song_set.length; k++)
      {
       // html += "" + album.song_set[j].song + "<br> ";
        html += '<li class=" song popular_item" id="song_'+artist.album_set[j].song_set[k].id+'"> <div id="p_song_name">'+ artist.album_set[j].song_set[k].id_no +' '+ artist.album_set[j].song_set[k].song +'</div>'
                +   ' <div class="miniIcons" id="p_alb_controls">'
                +       '<a href=""></a>' 
                +       '<a href=""></a>' 
                +       '<a href=""></a>' 
                +    '</li>';

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
      song_ready();
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
                    $('#playlists').prepend('<li><span>'+val+'</span></li>');
                   // $('#playlist_new').empty();
                     $('#playlist_new').html('<div id="plus_icon"><i class="icon-plus"></i></div><div id="create_new_div"><a id="create_new">Create New</a></div>');
                   /*  $.ajax({
                        type: 'post',
                        url: 'playlist/',
                        data: {'name':val} 
                       });
                     */
                   $.post('playlist/',{name:val});  
                     val=null;

                     //   }
                     $("#playlist_new").bind("click",create_playlist);
                  // console.log($('#create_new'));
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
  url = 'playlist/';
  $.ajax(url,{ type:"GET" } ,contentType= "application/json").done( function(data){
      $("#centerdata").empty();
        $("#centerdata").append('<div id="playlistsList">  <div class="nano" id="left_playlist_list">  <div id="contentList" class="content"> </div></div></div>');
      if(data.active)
      {
        html = '<div class="start"><div class="list_alpha"><div class="playlist" id="playlist_new"><div id="plus_icon"><i class="icon-plus"></i></div><div id="create_new_div"><a id="create_new">Create New</a></div></div> <ul id= "playlists"></ul></div></div>';
      $("#contentList").append(html);
      for(var i=0; i<data.playlists.length; i++){
        var playlist = data.playlists[i];
        $("#playlists").append('<li><span class="playlist" id="playlist_'+ playlist.id +'">'+playlist.name+'</span></li>');
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
    }
    /*
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

function display_playlist(id){
  url = "playlist/" + id;
    $.ajax(url,contentType= "application/json").done( function(data){
      if(!data.active)
      {
        console.log('No playlist Bro');
       return; 
      }
      playlist = data.playlist;
      if(playlist.songs){
        songs = playlist.songs.split('b');
        songs_list = playlist.songs_list;
        html = "<br> playlist Name: <br>" + playlist.name + "<br> Songs: " + songs.length + "<br>private : " + playlist.private;
        $("#append").append(html);
        for(var i=0; i<songs.length; i++)
        {
            html = "<br> i=" + songs[i] + " : "+ playlist.songs_list[songs[i]] + "<br>";
            $("#append").append(html); // append must be in callback as it would be called after ajax request
        }
      }
      else{
      $("#append").append("No Songs");
      }
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
  var html1 = "<div class='item_wrapper playable' id='song_"+k+"' data-type='play' data-value='"+k+"'>"+
    '<div class="item song"  id="song_'+k+'" style="background:url('+'\'\/media\/' + album_art +  '\'); background-size:cover">' +
   ' <div id="faint"></div>'+
   ' <a class="play_icon"><i class="icon-play song-icon-play"></i></a>'+
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
  //  console.log(html1);
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
    console.log('new ' + prev_artist +' ' + artisttag_count);
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
  $(artisttag_id).append('<li><span class="artist" id="artist_'+ artist.id +'">'+name+'</span></li>');
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
    console.log('new ' + prev_album +' ' + albumtag_count);
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
  $(albumtag_id).append('<li><span class="album" id="album_'+ album.id +'">'+name+'</span></li>');
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

function play(id)
{
  var url = "play/?song_id=" + id;
  var song_id = "#count_" + id;
  $.ajax(url,contentType= "application/json").done( function(data){
    var song = data[0];
    $("#musicPlayerPic").empty();
   $("#musicPlayerPic").append('<img src="\/media\/' + song.album.album_art +  '" style="width: 32px; height: 32px;" >');
   Jukebox.play_url('song_'+id,'http://192.168.121.5'+song.file_name)
 $("#ilSong").html('<b>'+song.song+'</b>');
  var art = [];
  for(i=0;i<song.artists.length && i<5; i++) art.push(song.artists[i].artist);
  $("#ilArtist").html('- '+art.join(' ,'));
   // $(song_id).html(song.count);
    song_playing = id;
    song_ready();
  });
}


function check_hash( name )
{
  hash = document.location.href.split('#')[1];
  if(!hash) hash="";
  hash = hash.replace(/\/$/, '');
  if(!prev_hash) prev_hash="";
  prev_hash = prev_hash.replace(/\/$/, '');
  console.log('prev_hash i123 '+ prev_hash);
  console.log('hash '+ hash);
  hash = hash.split('/');
  phash = prev_hash.split('/');
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
  else if(name=='artists' || name=='albums')
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
  console.log('hash      '+hash);
  hash = hash.split('/');
  name = hash[0];
  song = hash.indexOf('song');
  console.log(check_hash('song'));
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
  if( name == 'playlists') display_playlists();
  if( name == 'playlist' ) display_playlist(Number(hash[1]));
  if( name== 'search'){
    //$('#searchButton').click();
    //alert('hash   '+hash[1]);
    if(hash[1]=='') 
    {
      $("#songSearch").empty();
      $("#albumSearch").empty();
      $("#artistSearch").empty();
    }
    else
    {
      search(hash[1]);
    }
  }
  if (song >= 0){
    play(hash[song+1]);
  }
  prev_hash = document.location.href.split('#')[1];
}


$( document ).ready(function() {
  hash = document.location.href.split('#')[1];
  if(!hash)
  {
    hash_change('trending');
  }

  });

window.onload = split_hash();
window.onhashchange = split_hash(); // For IE<8 and safari
$(window).on('hashchange', function() {split_hash();});







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
      hash_change('playlist',id);
    });
}

function song_ready()
{
  $(".song").on('click',function(){
      id = $(this).attr('id').split('_')[1];
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
    });

}
