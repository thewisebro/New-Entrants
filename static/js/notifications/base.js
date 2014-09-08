(function() {

namespace("notifications", notification_clicked);

var notifications = Array();
var notifications_per_request = 20;
var more_notifications = true;
var notifications_pulling_interval = 60*1000; // 1 minute


$(document).on("load_app_notifications", function(e){
  if(!user.is_authenticated){
    nucleus.redirect_to_home();
    return;
  }
  nucleus.make_tabs_inactive();
  load_notifications_page();
});

$(document).on("unload_app_notifications", function(e){
  nucleus.make_tabs_active();
});

$(document).on("logout", function(){
  notifications = Array();
  more_notifications = true;
  not_viewed = null;
  if(nucleus.get_current_app() == 'notifications'){
    nucleus.redirect_to_home();
  }
});

function load_notifications_page(){
  $('#content').html("<div class='app-heading'>Notifications</div><div id='notifications'></div>");
  if(notifications.length === 0){
    update_notifications('first');
    setInterval(function(){
        update_notifications('previous');
      }, notifications_pulling_interval
    );
  }
  else{
    display_add_notifications('end', notifications);
  }
  //load_events_birthdays();
}

function update_notifications(action, number){
  if(action == 'previous'){
    if(notifications.length === 0)
      return;
    //showLoading = false;
  }
  $.get("/notifications/fetch",
    {'action' : action,
     'id' : action == 'previous' ? notifications[0].id : (notifications.length ? notifications[notifications.length-1].id : null),
     'number' : action == 'previous' ? '' : notifications_per_request
    },
    function(data){
      if(action != 'previous'){
        notifications = notifications.concat(data.notifications);
        more_notifications = data.more?true:false;
        if(nucleus.get_current_app() == 'notifications')
          display_add_notifications('end',data.notifications);
      }
      else{
        notifications = data.notifications.concat(notifications);
        if(nucleus.get_current_app() == 'notifications')
          display_add_notifications('start',data.notifications);
      }
      show_not_viewed_count(data.not_viewed);
    }
  );
}

function display_add_notifications(position,notifications){
 for(var i=0;i<notifications.length;i++){
//   try{
     if(position == 'end')
       $('#notifications').append(notification_html(notifications[i]));
     else
       $('#notifications').prepend(notification_html(notifications[notifications.length-i-1]));
//   }
//   catch(e){
//     console.log(e);
//   }
 }
 $('#notifications').pickify_users();
 if(more_notifications && $('#see-more-notifications').length === 0){
   $('#content').append("<div id='see-more-notifications' class='see-more'><span class='button2' onclick='see_more_notifications();'>See More</span></div>");
 }
 if(!more_notifications && $('#see-more-notifications').length==1){
  $('#see-more-notifications').css('display','none');
 }
}

function see_more_notifications(){
  update_notifications('next');
}

function notification_html(notification){
  return ""+
    "<div class='notification-box"+(!notification.viewed?" notification-box-not-viewed":"")+"' "+(notification.url?"style='cursor:pointer;' ":"")+
    "onclick='notifications.notification_clicked("+notification.id+");'>"+
      "<div class='notification-text'>"+(notification.app in channeli_apps?
        "<a target='_blank' href='"+channeli_apps[notification.app].url+"'>"+channeli_apps[notification.app].name+"</a>: ":"")+
        notification.content+"</div>"+
      "<div class='notification-time'>"+prettyDate(notification.datetime)+"</div><div style='clear:both'></div>"+
    "</div>";
}

function show_not_viewed_count(not_viewed){
  var elem = $('#notifications-count');
  elem.html(not_viewed);
  if(not_viewed>0)
    elem.removeClass('notifications-count-inact');
  else
    elem.addClass('notifications-count-inact');
}

function notification_clicked(notification_id){
  var notification = notifications.filter(function(ntfn){return ntfn.id == notification_id;})[0];
  if(notification.url){
    if(notification.url.substr(0,10) == '/birthday/'){
      birthday_wish_reply(notification.url);
    }
    else if(notification.url[0] == '#')
      location = notification.url;
    else
      window.open(notification.url,'_blank');
  }
}

function birthday_wish_reply(url){
  dialog_iframe({
    title : 'Reply',
    name:'birthday_reply_dialog',
    width:450,
    height:230,
    src:url
  });
}

})();
