var events = Array();
var events_per_request = items_per_request;
var more_events=true;

function update_events(action){
  var id = null;
  if(action == 'next')
    id = events[events.length-1].id;
  $.post("/events/fetch",
    {'calendar_name':'groups',
     'group_name':calendar_name,
     'action' : action,
     'id' : id,  
     'number' : events_per_request,
     'by_month_year' : '',
     'month' : '',
     'year' : ''
    },
    function(data){
      if(action != 'previous'){
        events = events.concat(data.events);
        more_events = data.more?true:false;
        display_add_events('end',data.events);
      }
    }  
  );
}

function display_add_events(position,events){
 for(var i=0;i<events.length;i++){
   try{
     if(position == 'end')
       $('#events').append(event_html(events[i]));
     else
       $('#events').prepend(event_html(events[events.length-i-1]));
   }
   catch(e){
     console.log(e);
   }
 }
 if(more_events && $('#see-more-events').length==0){
   $('#content-down').append("<div id='see-more-events' class='see-more'><span class='button2' onclick='see_more_events();'>See More</span></div>");
 }
 if(!more_events && $('#see-more-events').length==1){
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
