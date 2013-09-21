/* Base.js for basic javascript of jukebox*/


$("#trending").click(function(){ display("trending"); });
$("#artists").click(function(){ display("artists"); });
$("#albums").click(function(){ display("albums"); });







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
  url = 'playlist/';
  $.ajax(url,{ type:"GET", data: {user:user} } ,contentType= "application/json").done( function(data){
    $("#append").empty();
    html = 'Playlists: ';
    for(var i=0; i<data.length; i++){
      html += "<div onclick='display_playlist(" + data[i].id + ");'> Playlist Name: " + data[i].name + "</div>";
    }
    $("#append").append(html);
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
    "<br> <a href='#song_" + song.id + "' onclick='play(" + song.id + ");'>Play </a> <br><br>";
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
  var url = "play/?song_id=" + id;
  var song_id = "#song_" + id;
  $.ajax(url,contentType= "application/json").done( function(data){
    var song = data[0];
    $(song_id).html(song.count);
  });
}
