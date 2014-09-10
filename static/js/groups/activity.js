var activities = Array();
var activities_per_request = 20;
var more_activities=true;

function update_activities(action){
  $.post("/groups/fetch_activities",
    {'action' : action,
     'id' : (activities.length ? activities[activities.length-1].id : null),
     'number' : activities_per_request,
     'group_username':group_username,
    },
    function(data){
        activities = activities.concat(data.activities);
        console.log(activities);
        more_activities = data.more?true:false;
        display_add_activities('end',data.activities);
    }  
  );
}

function activity_html(activity){
  return ""+
    "<div class='feed-box'>"+
      "<img class='feed-propic' src='/photo/"+group_username+"/'/>"+
      "<div class='feed-heading'>"+group_name+"</div>"+
      "<div class='feed-right'>"+
        "<div class='feed-time'>"+prettyDate(activity.datetime)+"</div>"+
      "</div>"+
      "<div class='feed-text'>"+activity.text+"</div>"+
    "</div>";
}  

function display_add_activities(position,activities){
 for(var i=0;i<activities.length;i++){
//   try{
     if(position == 'end')
       $('#activities').append(activity_html(activities[i]));
     else
       $('#activities').prepend(activity_html(activities[activities.length-i-1]));
/*   }
   catch(e){
     console.log(e);
   }*/
 }
 $('#activities').pickify_users();
 if(more_activities && $('#see-more-activities').length==0){
   $('#groups-content').append("<div id='see-more-activities' class='see-more'><span class='button2' onclick='see_more_activities();'>See More</span></div>");
 }
 if(!more_activities && $('#see-more-activities').length==1){
  $('#see-more-activities').css('display','none');
 }
 if(!$('#activities').html())
   $('#activities').html("<div class='no-activities'>No Activity</div>");
} 

function see_more_activities(){
  update_activities('next');
} 

$('body').ready(function(){
  update_activities('first');
});
