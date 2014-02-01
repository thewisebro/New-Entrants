var calendars = null;
var events_per_request = 20;
var display_by_month_year = false;
var active_month, active_year;
var virtual_calendar;
var event_options_display_on = false;
var event_options_display_event_id = null;
var scroll_to_date;
var calendar_div_shown = false;

$(document).on("load_app_events", function(e){
  var hashtags = Array();
  for(var i=1;i<arguments.length;i++)
    hashtags.push(arguments[i]);
  load_events_page(hashtags);
});

function on_login_and_logout(){
  calendars = null;
  calendar_div_shown = false;
  virtual_calendar = null;
  if(get_current_app() == 'events'){
    load_events_page(get_app_hashtags());
  }
}

$(document).on('login', on_login_and_logout);
$(document).on('logout', on_login_and_logout);

function load_events_page(hashtags){
  $('#content').html(
      "<div id='events-header'>"+
        "<div id='events-type-header'></div>"+
        "<div id='refresh-button-div' class='button-div'>"+
          "<div class='button2' onclick='refresh_events();'>Refresh</div>"+
        "</div>"+
        "<div id='subscribe-button-div' class='button-div'></div>"+
        "<div id='home-button-div' class='button-div'>"+
          "<div class='button2' onclick='location.hash = \"events\";'>Upcoming events</div>"+
        "</div>"+
      "</div>"
  );
  $('#content').append("<div id='content-events'></div>");
  $('#content').append('<div id="add-event"></div>');
  if(!calendar_div_shown){
    $('#right-column .content').html(
      '<div id="calendar-div">'+
        '<div id="calendar">'+
          '<div id="month-bar">'+
            '<div id="month-name">'+
            '</div>'+
            '<div id="month-nav"><div onclick="previous_month();">&lt;</div> <div onclick="next_month();">&gt;</div>'+
            '</div>'+
          '</div>'+
          '<div id="week-bar">'+
          '</div>'+
          '<div id="date-matrix">'+
          '</div>'+
        '</div>'+
        (user_logged_in?
        '<div id="add-event-div">'+
          '<div class="div-button" onclick="add_event();">Add an event</div>'+
        '</div>':'')+
        '<div id="labels">'+
          '<div id="labels-header">Calendars</div>'+
          '<div id="labels-body">'+
          '</div>'+
        '</div>'+
      '</div>'
    );
    calendar_div_shown = true;
  }
  if(!calendars){
    get_calendars(hashtags);
    set_calendar();
  }
  else{
    process_hashtags(hashtags);
  }
  $('body').bind('click',function(e){
      $('.event-options-pop-up').hide();
      event_options_display_on = false;
    }
  );
}

function process_hashtags(hashtags){
  if(calendars.some(function(cal){return cal.name==hashtags[0];})){
    var calendar_name = hashtags.shift();
    if(hashtags.length>0){
      if(hashtags.length==3 && virtual_calendar){
        scroll_to_date = hashtags[2];
        if(active_year == hashtags[0] && active_month == hashtags[1] && display_by_month_year){
          display_add_events('first',virtual_calendar.events,virtual_calendar);
          return;
        }
      }
      else
        scroll_to_date = null;
      active_year = hashtags[0];
      active_month = hashtags[1];
      display_by_month_year = true;
      virtual_calendar = {
        name:'virtual_calendar',
        verbose_name:Months[active_month-1]+' '+active_year+' : '+get_calendar_from_name(calendar_name).verbose_name,
        more:true,
        events:Array(),
        calendar_name:calendar_name
      };
      change_active_label(calendar_name);
      update_events(virtual_calendar,'first',events_per_request);
    }
    else{
      display_by_month_year = false;
      load_calendar(calendar_name);
    }
  }
  else{
      display_by_month_year = false;
      load_calendar('all');
  }
}

function get_calendars(hashtags){
  $.get("/events/get_calendars",{},
    function(data){
        calendars = data.calendars;
        show_calendar_labels();
        for(var i=0;i<calendars.length;i++){
          calendars[i].more  = true;
          calendars[i].events = Array();
        }
        process_hashtags(hashtags);
    }
  );
}

function show_calendar_labels(){
  $('#labels-body').html('');
  for(var i=0;i<calendars.length;i++){
    $('#labels-body').append("<div id='label_"+calendars[i].name+"' class='label' onclick='label_clicked(\""+calendars[i].name+"\");'>"+
        "<div class='label-name'>"+calendars[i].verbose_name+"</div></div>");
  }
}

function label_clicked(calendar_name){
  if(display_by_month_year){
    location.hash = 'events/'+calendar_name+'/'+active_year+'/'+active_month;
  }
  else
    location.hash = 'events/'+calendar_name;
}

function change_active_label(calendar_name){
  for(var i=0;i<calendars.length;i++)
    $('#label_'+calendars[i].name). removeClass('active-label');
  $('#label_'+calendar_name). addClass('active-label');
}

function load_calendar(calendar_name){
  var calendar = get_calendar_from_name(calendar_name);
  change_active_label(calendar_name);
  $('#content-events').html('');
  if(calendar.events.length==0){
    update_events(calendar,'first',events_per_request);
  }
  else{
    display_add_events('end',calendar.events,calendar);
  }
}

function update_events(calendar,action,number){
  var id = null;
  if(action == 'next')
    id = calendar.events[calendar.events.length-1].id;
  $.get("/events/fetch",
    {'calendar_name':(calendar == virtual_calendar?virtual_calendar.calendar_name:calendar.name),
     'action' : action,
     'id' : id,
     'number' : number,
     'by_month_year' : (display_by_month_year?true:''),
     'month' : active_month,
     'year' : active_year
    },
    function(data){
      if(action!='previous'){
        calendar.events = calendar.events.concat(data.events);
        calendar.more = data.more?true:false;
        display_add_events('end',data.events,calendar);
      }
    }
  );
}

function event_html(Event,calendar_name){
  var html =
    "<div class='event-container' id='event-container"+Event.id+"' onmouseover='event_container_mouse_over("+Event.id+");'"+
                                 " onmouseout='event_container_mouse_out("+Event.id+");'>"+
      "<div class='event-type-head'>"+
        Event.date+(Event.weekday ? ' , '+Weekdays[Event.weekday]+'' : '')+
         "<div class='event-shown-calendar-name'><div class='event-options-icon-wrapper'>"+
         (Event.editable?"<div class='event-options-icon-wrapper-inside' onclick='show_event_options(this,event);'>"+
         "<div class='event-options-icon' id='event-options"+Event.id+"'>&#9660;</div></div>"+
         "<div style='clear:both'></div><div class='event-options-pop-up'><div onclick='edit_event("+Event.id+",event);'>Edit</div>"+
         "<div onclick='delete_event("+Event.id+",event);'>Delete</div></div>":"")+
         "</div>"+(calendar_name=='all' || (calendar_name=='virtual_calendar' && virtual_calendar.calendar_name == 'all')?
         "<div class='shown-cal-name' "+(Event.shown_calendar_name=='Groups Calendar'?"style='color:#43b167'":"")
           +">"+Event.shown_calendar_name+"</div>":"")+
         "</div>"+
      "</div> "+
      "<div class='event'>"+
        "<div class='event-time-title'>"+
          "<div class='event-time'>"+(Event.time?Event.time:"Event Title")+"</div>"+
          "<div class='event-name'>"+Event.title+"</div>"+
          "<div style='clear:both'></div>"+
        "</div>"
  if(Event.duration)
    html+=
        "<div class='event-duration'>"+
          "<div class='event-left'>Duration</div>"+
          "<div class='event-right'>"+Event.duration+"</div>"+
          "<div style='clear:both'></div>"+
        "</div>"

  if(Event.added_by)
    html+=
        "<div class='event-by'>"+
          "<div class='event-left'>By</div>"+
          "<div class='event-right'>"+Event.added_by+"</div>"+
          "<div style='clear:both'></div>"+
        "</div>"
  if(Event.place)
    html+=
        "<div class='event-place'>"+
          "<div class='event-left'><div title='Venue' class='event-place-icon'></div></div>"+
          "<div class='event-right'>"+Event.place+"</div>"+
          "<div style='clear:both'></div>"+
        "</div>"
  if(Event.description)
    html+=
        "<div class='event-short-description'>"+
          "<div class='event-left'><div title='Description' class='event-detail-icon'></div></div>"+
          "<div class='event-right'>"+Event.description+"</div>"+
          "<div style='clear:both'></div>"+
        "</div>"
  html+=
      "</div>"+
    "</div> ";
  return html;
}

function get_calendar_from_name(calendar_name){
 if(calendar_name == 'virtual_calendar')
   return virtual_calendar;
 for(var i=0;i<calendars.length;i++){
   if(calendars[i].name == calendar_name){
     return calendars[i];
   }
 }
}

function display_add_events(position,events,calendar){
 $('#events-type-header').html(calendar.verbose_name+' Events');
 if(calendar.name == 'virtual_calendar')
   $('#home-button-div').show();
 else
   $('#home-button-div').hide();
 var scroll_to_event_id;
 for(var i=0;i<events.length;i++){
   try{
     $('#content-events').append(event_html(events[i],calendar.name));
     if(!scroll_to_event_id && (new Date(events[i].date)).getDate() == scroll_to_date)scroll_to_event_id = events[i].id;
   }
   catch(e){
     console.log(e);
   }
 }
 //$('#content-events').pickify_users();
 if(calendar.more == true && $('#see-more-events').length==0){
   $('#content').append("<div id='see-more-events' class='see-more'><span class='button2' onclick='see_more_events(\""+calendar.name+"\");'>See More</span></div>");
 }
 if(calendar.more == false && $('#see-more-events').length>0){
   $('#see-more-events').remove();
 }
 $('.event-right').find('img').click(function(){
     $.fancybox($(this).attr('src'));
   }
 );
 if(scroll_to_event_id)
  $('body').animate({scrollTop:$('#event-container'+scroll_to_event_id).offset().top-$('#content').offset().top},250);
 if(!$('#content-events').html()){
   $('#content-events').html("<div class='no-events'>No Events</div>");
 }
}
function see_more_events(calendar_name){
  var calendar = get_calendar_from_name(calendar_name);
  update_events(calendar,'next',events_per_request);
}

var today = new Date(),display_month=null,display_year=null;

function getFirstDay(theYear, theMonth){
    var firstDate = new Date(theYear,theMonth,1)
    return (firstDate.getDay()+6)%7; // Monday as 0
}
function getMonthLen(theYear, theMonth) {
    var oneDay = 1000 * 60 * 60 * 24
    var thisMonth = new Date(theYear, theMonth, 1)
    var nextMonth = new Date(theYear, theMonth + 1, 1)
    var len = Math.ceil((nextMonth.getTime() -
        thisMonth.getTime())/oneDay)
    return len;
}

var Months = ["January","February","March","April","May","June","July","August",
"September","October","November","December"];
var Weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'];

function set_calendar(){
  if(display_month == null) display_month = today.getMonth();
  if(display_year == null) display_year = today.getFullYear();
  $.get('/events/get_events_dates',{
      month : display_month+1,
      year : display_year
    },
    function(data){
      $('#week-bar').html('<div>Mon</div><div>Tue</div><div>Wed</div><div>Thu</div><div>Fri</div><div>Sat</div><div>Sun</div>');
      var dates = data.dates;
      var first_day = getFirstDay(display_year,display_month);
      $('#month-name').html("<div onclick='location.hash=\"events/all/"+(display_year)+"/"+(display_month+1)
                       +"\"'>"+Months[display_month].toUpperCase()+" "+display_year+"</div>");
      $('#date-matrix').html('');
      for(var i=0;i<first_day;i++)
        $('#date-matrix').append("<div></div>");
      for(var i=0;i<getMonthLen(display_year,display_month);i++){
        if((i+1) == today.getDate() && display_month == today.getMonth() && display_year == today.getFullYear())
          $('#date-matrix').append("<div class='today'>"+(i+1)+"</div>");
        else if(dates.some(function(date){return date==(i+1);}))
          $('#date-matrix').append("<div class='event-day' onclick='location.hash=\"events/all/"+
            (display_year)+"/"+(display_month+1)+"/"+(i+1)+"\"'>"+(i+1)+"</div>");
        else
          $('#date-matrix').append("<div>"+(i+1)+"</div>");
      }
    }
  );
}

function previous_month(){
  if(display_month>0){
    display_month -= 1;
  }
  else{
    display_year -=1;
    display_month = 11;
  }
  set_calendar();
}

function next_month(){
  if(display_month<11){
    display_month += 1;
  }
  else{
    display_year +=1;
    display_month = 0;
  }
  set_calendar();
}

function add_event(){
  dialog_iframe({
    name:'add_event_dialog',
    title:'Add event',
    height:700,
    width:920,
    src:'/events/add/'
  });
}

function show_event_options(element,e){
  if(e.stopPropagation)
    e.stopPropagation();
  else
    e.cancelBubble = true;
  if(!event_options_display_on){
    $(element).parent().find('.event-options-pop-up').show();
    event_options_display_on = true;
    event_options_display_event_id = $(element).children()[0].id.substr(13);
  }
  else{
    $(element).parent().find('.event-options-pop-up').hide();
    event_options_display_on = false;
  }
}

function event_container_mouse_over(event_id){
  if(event_id != null && event_id != event_options_display_event_id){
    setTimeout(function(){$('#event-options'+event_options_display_event_id).hide();},500);
    $('.event-options-pop-up').hide();
    event_options_display_on = false;
  }
  $('#event-options'+event_id).show();
}

function event_container_mouse_out(event_id){
  if(!event_options_display_on)
   $('#event-options'+event_id).hide();
}

function delete_event(event_id,e){
  if(e.stopPropagation)
    e.stopPropagation();
  else
    e.cancelBubble = true;
  if($('#delete-event-confirm').length == 0)
    $('body').append("<div id='delete-event-confirm' title='Delete this event?' style='display:none'>"+
      "<p><span class='ui-icon ui-icon-alert' style='float: left; margin: 0 7px 20px 0;'></span>This event will be permanently deleted and cannot be recovered. Are you sure?</p></div>");

  $( "#delete-event-confirm" ).dialog({
    resizable: false,
    height:180,
    modal: true,
    buttons: {
      "Delete this event": function() {
        $.post('/events/delete/',{
            id:event_id
          },function(data){
            if(data.result == 'success'){
              var all_calendars = calendars.concat(virtual_calendar);
              for(var i=0;i<all_calendars.length;i++){
                try{
                  var events = all_calendars[i].events;
                  var Event = events.filter(function(ev){return ev.id == event_id;})[0];
                  events.splice(events.indexOf(Event),1);
                }catch(e){}
              }
              $('#event-container'+event_id).slideToggle('fast');
            }
          }
        );
        $( this ).dialog( "close" );
      },
      Cancel: function() {
        $( this ).dialog( "close" );
      }
    }
  });
}

function edit_event(event_id,e){
  if(e.stopPropagation)
    e.stopPropagation();
  else
    e.cancelBubble = true;
  dialog_iframe({
    name:'edit_event_dialog',
    title:'Edit event',
    height:700,
    width:920,
    src:'/events/edit/'+event_id+'/'
  });
}

function refresh_events(){
  calendars = null;
  virtual_calendar = null;
  try{
    upcoming_events = Array();
  }catch(e){}
  var hashtags = location.hash.substr(1).split('/');
  var first_hashtag = hashtags.shift();
  load_events_page(hashtags);
}
