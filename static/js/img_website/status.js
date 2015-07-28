var counter_initial = 0;
var status_count_per_request = 20
var counter_final = status_count_per_request;
var monthNames = [ "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December" ];
function get_nth_suffix(date) {
  switch (date) {
    case 1:
    case 21:
    case 31:
      return 'st';
    case 2:
    case 22:
      return 'nd';
    case 3:
    case 23:
      return 'rd';
    default:
      return 'th';
  }
}
$(document).ready(function(){
  $('#previous').on('click',function(){
      counter_initial = counter_initial + status_count_per_request;
      counter_final = counter_final + status_count_per_request;
      getPosts();
  });
});

getPosts();
//window.setInterval(function(){getPosts();}, 3000);
function getPosts(){
  var html_to_append = '';
  $.getJSON(status_ajax_url, function(data){
      //console.log(data);
      //console.log(counter);
      if(data.length<=counter_final){
        counter_final = data.length;
      }
      for(var i=counter_initial;i<counter_final;i++)
      {
        //date_created = new Date(data[i].fields.date);
        //date_string = monthNames[date_created.getMonth()] + ' ' + date_created.getDate() + get_nth_suffix(date_created.getDate()) + ', ' + date_created.getFullYear() + ' ' + date_created.toLocaleTimeString();
        html_to_append +='<div class="span9 article"><div class="article_title"><span class="app_name">' + data[i].app + '</span><span class="date_status">' + data[i].date + '</span></div><div class="article_content"><div class="article_content_text">' + data[i].content + '<br/></div><!--<div class="article_content_image"></div> --></div> <!-- end article_content --></div> <!-- end article --><hr class="hr_status"/>';
        //console.log(data[i].pk);
      }
      $('.articles_list').append(html_to_append);
      if(data.length<=counter_final){
        $('#previous').hide();
      }
      else
      {
        $('#previous').show();
      }

  });
}

