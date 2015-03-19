var links = null;

function load_handler(e){
  var tab = nucleus.get_current_app();
  if(!links){
    $.get("/get_links/", function(data){
        links = data;
        pre_process_links();
        show_links(tab);
    });
  }
  else
    show_links(tab);
  show_default_right_column();
}

function unload_handler(e){
};

$(document).on("load_app_apps", load_handler);
$(document).on("load_app_games", load_handler);
$(document).on("load_app_links", load_handler);

$(document).on("unload_app_apps", unload_handler);
$(document).on("unload_app_games", unload_handler);
$(document).on("unload_app_links", unload_handler);

function pre_process_links(){
  for(var i=0; i<links.apps.length;i++){
    var d = links.apps[i];
    links.apps[i] = {
      'app': d[0],
      'app_data': d[1]
    };
    links.apps[i]['target_blank'] = links.apps[i]['app_data'].url.indexOf('#')==-1;
  }
  for(var i=0; i<links.games.length;i++){
    var d = links.games[i];
    links.games[i] = {
      'game': d[0],
      'game_data': d[1]
    };
  }
}

function show_links(tab){
  if(tab == 'apps')
    $('#content').html(Handlebars.nucleus_templates.apps(links));
  else if(tab == 'games')
    $('#content').html(Handlebars.nucleus_templates.games(links));
  else if(tab == 'links')
    $('#content').html(Handlebars.nucleus_templates.links(links));
}

function show_default_right_column(){
  var $eb_div = $('#events-birthdays');
  if($eb_div.length == 0){
    $('#right-column .content').html("<div id='events-birthdays'></div>");
    load_events_birthdays();
  }
}




/* right column js */

var no_of_upcoming_events = 3;
var upcoming_events = Array();
var birthday_users = Array();
var todays_menu = null;

function load_events_birthdays(){
  $('#events-birthdays').html("</div><div id='birthdays' class='right-box'></div>"+
      "<div id='menu' class='right-box'></div>"+
      "<div id='upcoming-events' class='right-box'></div>"
      );
  events_birthdays();
}

function nucleus_on_login_logout(){
  upcoming_events = Array();
  birthday_users = Array();
  todays_menu = null;
  links = null;
  load_handler();
  var $eb_div = $('#events-birthdays');
  if($eb_div.length != 0)
    load_events_birthdays();
}

$(document).on("login", nucleus_on_login_logout);
$(document).on("logout", nucleus_on_login_logout);

function events_birthdays(){
  if(user.is_authenticated){
    if(birthday_users.length == 0){
      $.get("/birthday/today",{},function(data){
          birthday_users = data.birthday_users;
          if(birthday_users.length)
            display_birthdays();
        }
      );
    }
    else{
      display_birthdays();
    }
  }
  if(upcoming_events.length == 0){
    $.get("/events/fetch",
      {'calendar_name':'all',
       'action' : 'first',
       'number' : no_of_upcoming_events,
       'by_month_year' : '',
       'id':''
      },
      function(data){
        upcoming_events = data.events;
        display_upcoming_events();
      }
    );
  }
  else{
    display_upcoming_events();
  }
  if(todays_menu === null){
    $.get("/messmenu/todays_menu/",
      {},
      function(data){
        todays_menu = data;
        display_menu();
    });
  }
  else if(todays_menu.length > 0){
    display_menu();
  }
}

function display_upcoming_events(){
  $('#upcoming-events').show();
  $('#upcoming-events').html(""+
    "<div class='right-content-title'>Upcoming Events</div>"+
    "<div class='right-content-information' id='upcoming-events-boxes'></div>"+
    "<div class='right-content-see-more'>"+
      "<span onclick='location.hash=\"events\";'>See All</span>"+
    "</div>"
  );
  for(var i=0;i < upcoming_events.length && i < no_of_upcoming_events;i++){
    var html = ""+
      "<div class='event-box' onclick='location.hash=\"events\";'>"+
        "<div class='event-name1'>"+upcoming_events[i].title+"</div>"+
        "<div class='event-date1'><span class='date'>"+upcoming_events[i].date+
        "</span>"+(upcoming_events[i].time?" at <span class='time'>"+
            upcoming_events[i].time+"</span>":"")+"</div>"+
      "</div>";
    $('#upcoming-events-boxes').append(html);
  }
}

function display_birthdays(){
  $('#birthdays').show();
  $('#birthdays').html(""+
    "<div class='right-content-title'>Birthdays Today</div>"+
    "<div class='right-content-information' id='birthday-boxes'></div>"
  );
  for(var i=0;i < birthday_users.length;i++){
    var html = ""+
      "<div class='event-box' "+
          (i==birthday_users.length-1?"style='border-bottom:0px'":'')+' '+
          "onclick='birthday_wish(\""+birthday_users[i].user.username+"\",\""+birthday_users[i].user.name+"\");'>"+
        "<div class='event-name1'>"+user_html_name(birthday_users[i].user)+"</div>"+
      "</div>";
    $('#birthday-boxes').append(html);
  }
  $('#birthday-boxes').pickify_users();
}

function display_menu(){
  if(todays_menu.length > 0){
    $('#menu').show();
    $('#menu').html(""+
      "<div class='right-content-title'>Today's Mess Menu</div>"+
      "<div class='right-content-information' id='menu-boxes'></div>"
    );
    var time_of_day_map = {
      1: 'Breakfast',
      2: 'Lunch',
      3: 'Dinner'
    };
    for(var i=1; i<=3; i++) {
      if(todays_menu.filter(function(a){return a.time_of_day==i}).length > 0) {
        var html = ""+
          "<div class='event-box' onclick='location=\"/messmenu/\";'>"+
            "<div class='event-name1'><span class='time_of_day'>"+time_of_day_map[i]+": </span>"+
            "<span class='menu-content'>"+todays_menu.filter(function(a){return a.time_of_day==i})[0].content+
            "</span></div>"+
          "</div>";
        $('#menu-boxes').append(html);
      }
    }
  }
}

function birthday_wish(username,name){
  dialog_iframe({
    name:'birthday_wish_dialog',
    title:'Wish '+name,
    width:450,
    height:230,
    src:'/birthday/wish/'+username+'/'
  });
}

