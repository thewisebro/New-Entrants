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






var song_playing;
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
  $.ajax({
      type: 'get',
      url: 'search?q='+q,
      success: function (data) {
       $("#songSearch").empty();
       $("#songSearch").append('<div class="searchHeading">SONGS<span> (2,349)</span></div>');
       $("#songSearch").append('<div> <ul  id="songSearchSpan" class="searchResultList" > </ul> </div>');
       for(var i=0; i<data.songs.length; i++)
       {
         var html = '<li class="item song" id="song_'+data.songs[i].id+'"><div class="searchItemImg" ></div>'
                  +  '<div class="searchItemDetails">'
		              +   '<div class="itemName">'+ data.songs[i].song+'</div>'
		              +    '<div class="itemSubDetail">'+data.songs[i].artists[0].artist+'</div></div></li>';
         $("#songSearchSpan").append(html);
       }
       $("#albumSearch").empty();
       $("#albumSearch").append('<div class="searchHeading">Albums<span> (2,349)</span></div>');
       $("#albumSearch").append('<div> <ul  id="albumSearchSpan" class="searchResultList" > </ul> </div>');
       for(var i=0; i<data.albums.length; i++)
       {
         var html = '<li><div class="searchItemImg"></div>'
                  +  '<div class="searchItemDetails">'
		              +   '<div class="itemName">'+ data.albums[i].album+'</div>'
		              +    '<div class="itemSubDetail">'+data.albums[i].artists[0].artist+'</div></div></li>';
         $("#albumSearchSpan").append(html);
       }
       $("#artistSearch").empty();
       $("#artistSearch").append('<div class="searchHeading">Artists<span> (2,349)</span></div>');
       $("#artistSearch").append('<div> <ul  id="artistSearchSpan" class="searchResultList" > </ul> </div>');
       for(var i=0; i<data.artists.length; i++)
       {
         var html = '<li><div class="searchItemImg"></div>'
                  +  '<div class="searchItemDetails">'
		              +   '<div class="itemName">'+ data.artists[i].artist+'</div>'
		              +    '</div></li>';
         $("#artistSearchSpan").append(html);
       }
      artist_ready();
      album_ready();
      song_ready();
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
       $("#rightside").css('display','none');
     }
    if(name=='artists' || name=='albums')
    {
       $("#rightside").css('display','block');
      // console.log($(wi))
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
	      if(name=='albums' || name=='artists')
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
      }
      if(name=='albums')
      {
     //   console.log('yoooooooo');
       // $("#centerdata").append('</div></div></div>');
        $("#albumsList").append('<div id="oneAlbumOpened"><div id="oaoWrapper"></div></div>');
        $("#oneAlbumOpened").append('<div id="album_panel_hide"><i class="icon-reorder"></i></div>');
        lAlbums();
      }
      if(name=='artists')
      {
     //   console.log('yoooooooo');
       // $("#centerdata").append('</div></div></div>');
        $("#artistsList").append('<div id="artist_view"></div>');
        $("#artistsList").append('<div id="artist_panel_hide"><i class="icon-reorder"></i></div>');
        lArtists();
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
        html += '<li class="popular_item"> <div id="p_song_name">'+ album.song_set[j].song +'</div>'
                +   ' <div class="miniIcons" id="p_alb_controls">'
                +       '<a href=""></a>' 
                +       '<a href=""></a>' 
                +       '<a href=""></a>' 
                +    '</li>';

      }
      $("#popular_list").append(html);

      artist_ready();
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
        html += '<li class="popular_item"> <div id="p_song_name">'+ artist.album_set[j].song_set[k].song +'</div>'
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
    });

}


function display_playlists(user){
  url = 'playlist/';
  $.ajax(url,{ type:"GET", data: {user:user} } ,contentType= "application/json").done( function(data){
    $("#append").empty();
    html = 'Playlists: ';
    for(var i=0; i<data.length; i++){
      html += "<div onclick='hash_change('playlist',"  + data[i].id + ");'> Playlist Name: " + data[i].name + "</div>";
    }
    $("#append").append(html);
  });
}

function display_playlist(id){
  url = "playlist/" + id;
    $.ajax(url,contentType= "application/json").done( function(data){
      playlist = data;
      $("#append").empty();
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
   ' <div class="song_name"><b>' + album + '</b></div>' +
   ' <div class="artist_name">';  
   for (var j=0; j<song.artists.length; j++)
   {
     html1 += song.artists[j].artist + ", ";
   }
   html1 += '</div>'+
    '</div>' +
    '</div>';
    console.log(html1);
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
  tagg = 'Others';
  if(!artist.artist) return;
  var name = capitalize(artist.artist);
  if(!name[0].match(/^[A-Z]+$/)) tagg='Others';
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
  tagg = 'Others';
  if(!album.album) return;
  var name = capitalize(album.album);
  if(!name[0].match(/^[A-Z]+$/)) tagg='Others';
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
  if(!prev_hash) prev_hash="";
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
  hash = hash.split('/');
  name = hash[0];
  song = hash.indexOf('song');
  console.log(check_hash('song'));
  if(song>=0 && check_hash('song')){ play(hash[song+1]); prev_hash=document.location.href.split('#')[1]; console.log(hash[song+1]); return;}
  if ( Object.keys(names).indexOf(name) >= 0){
    if(hash.length == 2 || hash.length == 4){
      if(name == 'artists'){ if(!check_hash('artists')) display('artists'); display_artist(hash[1]); }
      if(name == 'albums'){ if(!check_hash('albums')) display('albums');  display_album(hash[1]); }
    }
    else{
      display(name);
    }
  }
  if( name == 'playlists') display_playlists(hash[1]);
  if( name == 'playlist' ) display_playlist(Number(hash[1]));
  if( name== 'search'){
    //$('#searchButton').click();
    alert('hash   '+hash[1]);
    search(hash[1]);
  }
  if (song >= 0){
    play(hash[song+1]);
  }
  prev_hash = document.location.href.split('#')[1];
}


window.onload = split_hash();
window.onhashchange = split_hash(); // For IE<8 and safari
$(window).on('hashchange', function() {split_hash();});







$("#trending_link").click(function(){ hash_change("trending"); });  // changes hash when trending is clicked
$("#artists_link").click(function(){ hash_change("artists"); });    // changes hash when Artist is clicked
$("#albums_link").click(function(){ hash_change("albums"); });      // changes hash when Albums is clicked

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
