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

$("#trending").click(function(){ display("trending"); });
$("#artists").click(function(){ display("artists"); });
$("#albums").click(function(){ display("albums"); });
$('form#playlist').on('submit', function(e) {
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
      }
      });
  e.preventDefault();
});






/************************************ Actual Work *******************************************/
// names-> for different urls working the same way
var names = {
  "trending" : ['trending/', 'get_song_html'],
  "albums" : ['albums/', 'get_album_html'],
  "artists" : ['artists/', 'get_artist_html']
};

// display function for display of list of either songs, artists or albums
function display(name){
  if (name in names){
    // for hashtags
    href = '#' + name;
    document.location.href = href;
    var show = names[name];
    var url = show[0];
    var func = window[show[1]];
    var items=[];
    $.ajax(url,contentType= "application/json").done( function(data){
      items=data;
      $("#append").empty();
      for (var i=0; i<items.length; i++){
        $("#append").append(func(items[i]));
      }
    });
  }
}


// display_album for displaying a specific album
function display_album(id){
  href = '#albums/'+ id;
  document.location.href = href;
  url = "albums/" + id;
    $.ajax(url,contentType= "application/json").done( function(data){
      album = data[0];
      $("#append").empty();
      html = "<br> Album Name: <br>" + album.album + "<br> Artists: ";
      for(var j=0; j<album.artists.length; j++)
      {
        html +="<div onclick='display_artist(" + album.artists[j].id + ");'>" + album.artists[j].artist + "</div> ";
      }
        html += "<br> <img src='/media/"+ album.album_art + "' width='300px' height='300px'> <br> <br> Songs: <br>";
      for(var j=0; j<album.song_set.length; j++)
      {
        html += "" + album.song_set[j].song + "<br> ";
      }
      $("#append").append(html);
    });

}



// display_artist for displaying a specific artist
function display_artist(id){
  href = '#artists/'+ id;
  document.location.href = href;
  url = "artists/" + id;
    $.ajax(url,contentType= "application/json").done( function(data){
      artist = data[0];
      $("#append").empty();
      html = "<br> Artist: <br>" +
        "Artist Name: " + artist.artist +
        "<br> <img src='/media/"+ artist.cover_pic + "' width='300px' height='300px'> <br> <br>" +
        "Albums: " + artist.album_set.length + "<br>";
      for(var j=0; j<artist.album_set.length; j++)
      {
        html += "<div class='artists' onclick='display_album(" + artist.album_set[j].id + ");'>" + artist.album_set[j].album +
        "<br> <img src='/media/"+ artist.album_set[j].album_art + "' width='100px' height='100px'> <br>" ;
      }
      $("#append").append(html);
    });

}


function display_playlists(user){
  href = '#playlists/' + user;
  document.location.href = href;
  url = 'playlist/';
  $.ajax(url,{ type:"GET", data: {user:user} } ,contentType= "application/json").done( function(data){
    $("#append").empty();
    html = 'Playlists: ';
    for(var i=0; i<data.length; i++){
      html += "<div onclick='display_playlist("  + data[i].id + ");'> Playlist Name: " + data[i].name + "</div>";
    }
    $("#append").append(html);
  });
}

function display_playlist(id){
  href = '#playlist/' + id;
  document.location.href = href;
  url = "playlist/" + id;
    $.ajax(url,contentType= "application/json").done( function(data){
      playlist = data;
      $("#append").empty();
      if(playlist.songs){
        songs = playlist.songs.split('b')
        html = "<br> playlist Name: <br>" + playlist.name + "<br> Songs: " + songs.length;
        $("#append").append(html);
        for(var i=0; i<songs.length; i++)
        {
          url = 'song/' + Number(songs[i]);
          $.ajax(url,contentType= "application/json").done( function(data){
            html = "<br> i=" + data.id + " : "+ data.song + "<br>";
            $("#append").append(html); // append must be in callback as it would be called after ajax request
          });
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
  html = "<br> Song: "+ song.song+ "<br> Album: " + song.album.album +"<br> Artist: ";
  for (var j=0; j<song.artists.length; j++)
  {
    html += song.artists[j].artist + ", ";
  }
  html += "<br> Count: <p id='song_" + song.id + "'>" + song.count + "</p> " +
    "<img src=\'\/media\/" + song.album.album_art + "\' width='100px' height='100px'>" +
    "<br> <span onclick='play(" + song.id + ");'>Play </span> <br><br>";
  return html;
}



// for 1 artist html
function get_artist_html(artist)
{
  html = "<div class='artists' onclick='display_artist(" + artist.id + ");'>" +
    "<br> Artist: "+ artist.artist +
    "<br> <img src='/media/" + artist.cover_pic + "' width='100px' height='100px'>" +
    "<br><br><br></div>";
  return html;
}


// for 1 album html
function get_album_html(album)
{
  html =  "<div class='albums' onclick='display_album(" + album.id + ")'>" +
    "<br> Album: "+ album.album + "<br> Artists:  ";
  for (var j=0; j<album.artists.length; j++)
  {
    html +=  album.artists[j].artist + ", ";
  }
    html += "<br> <img src=\'\/media\/" + album.album_art + "\' width='100px' height='100px'>" +
    "<br><br><br>";
  return html;
}

function play(id)
{
  hash = document.location.href.split('#')[1];
  hash = hash.split('/');
  if((i=hash.indexOf('song')) >=0 ){
    hash[i+1] = id;
    document.location.href = "#" +hash.join('/');
  }
  else{
    document.location.href += '/song/' + id;
  }
  var url = "play/?song_id=" + id;
  var song_id = "#song_" + id;
  $.ajax(url,contentType= "application/json").done( function(data){
    var song = data[0];
    $(song_id).html(song.count);
  });
}




function split_hash(){
  hash = document.location.href.split('#')[1];
  hash = hash.split('/');
  name = hash[0];
  song = hash.indexOf('song');
  if ( Object.keys(names).indexOf(name) >= 0){
    if(hash.length == 2){
      if(name == 'artists') display_artist(hash[1]);
      if(name == 'albums') display_album(hash[1]);
    }
    else{
      display(name);
    }
  }
  if( name == 'playlists') display_playlists(hash[1]);
  if( name == 'playlist' ) display_playlist(Number(hash[1]));
  if( name== 'search'){
    $("form#search").find("input[type=text]").val(hash[1]);
    $("form#search").submit();
  }
  if (song >= 0){
    play(hash[song+1]);
  }
}


window.onload = split_hash();
window.onhashchange = split_hash(); // For IE<8 and safari
$(window).on('hashchange', function() {split_hash();});







