var feeds = Array();
var feeds_per_request = 50;
var more_feeds = true;
var feeds_pulling_interval = 60*1000; // 1 minute

$(document).on("load_app_home", function(e){
  load_feeds_page();
});

function load_feeds_page(){
  $('#content').html("<div id='feeds'></div>");
  if(feeds.length === 0){
    update_feeds('first');
    setInterval(function(){update_feeds('previous');},feeds_pulling_interval);
  }
  else{
    display_add_feeds('end',feeds);
  }
  show_default_right_column();
}

function update_feeds(action,number){
  if(action == 'previous'){
    if(feeds.length === 0)
      return;
    showLoading = false;
  }
  $.get("/feeds/fetch",
    {'action' : action,
     'id' : action == 'previous' ? feeds[0].id : (feeds.length ? feeds[feeds.length-1].id : null),
     'number' : action == 'previous' ? '' : feeds_per_request
    },
    function(data){
      if(action != 'previous'){
        feeds = feeds.concat(data.feeds);
        more_feeds = data.more?true:false;
        if(nucleus.get_current_app() == 'home')
          display_add_feeds('end',data.feeds);
      }
      else{
        feeds = data.feeds.concat(feeds);
        if(nucleus.get_current_app() == 'home')
          display_add_feeds('start',data.feeds);
      }
    }
  );
}

function get_app_icon_url(app){
  var url = "/static/images/nucleus/app-icons/"+app+".png";
  return url;
}

function feed_html(feed){
  var $content = $(feed.content);
  var $feed_bottom = $('.feed-bottom', $content);
  if($feed_bottom.length > 0){
    var context = {
      feed: feed
    };
    if(feed.app in channeli_apps)
      context.app = channeli_apps[feed.app];
    context.date = prettyDate(feed.datetime);
    $feed_bottom.html(Handlebars.feeds_templates.bottom(context));
  }
  feed.content = $('<div>').append($content).html();
    return ""+
    "<div class='feed-box'>"+
      ('username' in feed?
        "<img class='feed-propic' src='/photo/"+feed.username+"/'/>"
        :("<a target='_blank' href="+channeli_apps[feed.app].url+">"+
          "<img class='feed-propic' src='"+get_app_icon_url(feed.app)+"'/>"+
          "</a>")
      )+
      "<div class='feed-text'>"+feed.content+"</div>"+
    "</div>";
}

function display_add_feeds(position,feeds){
 for(var i=0;i<feeds.length;i++){
//   try{
     if(position == 'end')
       $('#feeds').append(feed_html(feeds[i]));
     else
       $('#feeds').prepend(feed_html(feeds[feeds.length-i-1]));
//   }
//   catch(e){
//     console.log(e);
//   }
 }
 $('#feeds').pickify_users();
 $('.event-right').find('img').click(function(){
     $.fancybox($(this).attr('src'));
   }
 );
 if(more_feeds && $('#see-more-feeds').length === 0){
   $('#content').append("<div id='see-more-feeds' class='see-more'><span class='button2' onclick='see_more_feeds();'>See More</span></div>");
 }
 if(!more_feeds && $('#see-more-feeds').length==1){
  $('#see-more-feeds').css('display','none');
 }
}

function see_more_feeds(){
  update_feeds('next');
}
