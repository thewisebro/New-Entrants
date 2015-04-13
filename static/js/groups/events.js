var groups_events = Array();
var groups_events_per_request = items_per_request;
var more_groups_events=true;

function update_events(action){
  var id = null;
  if(action == 'next')
    id = groups_events[groups_events.length-1].id;
  $.post("/events/fetch",
    {'calendar_name':'groups',
     'group_name':calendar_name,
     'action' : action,
     'id' : id,
     'number' : groups_events_per_request,
     'by_month_year' : '',
     'month' : '',
     'year' : ''
    },
    function(data){
      if(action != 'previous'){
        groups_events = groups_events.concat(data.events);
        more_events = data.more?true:false;
        display_add_events('end',data.events);
      }
    }
  );
}

function display_add_events(position,groups_events){
 for(var i=0;i<groups_events.length;i++){
   try{
     if(position == 'end')
       $('#events').append(event_html(groups_events[i]));
     else
       $('#events').prepend(event_html(groups_events[groups_events.length-i-1]));
   }
   catch(e){
     console.log(e);
   }
 }
 if(more_groups_events && $('#see-more-events').length==0){
   $('#content-down').append("<div id='see-more-events' class='see-more'><span class='button2' onclick='see_more_events();'>See More</span></div>");
 }
 if(!more_groups_events && $('#see-more-events').length==1){
  $('#see-more-events').css('display','none');
 } 
 $('.event-right').find('img').click(function(){
     $.fancybox($(this).attr('src'));
   }
 );
 if(!$('#events').html())
   $('#events').html("<div class='no-events'>No Events</div>");
} 

function see_more_events(){
  update_events('next');
}  

$('body').ready(function(){
  update_events('first');
  $('body').bind('click',function(e){
      $('.event-options-pop-up').hide();
      event_options_display_on = false;
    }
  );
});
