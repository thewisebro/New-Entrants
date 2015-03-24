function subscribe(username,subscribed)
{
  url = "/groups/"+username+"/subscriber/" 
  $.post(url,
    {
      'subscribed':subscribed,
    },
    function(data){ 
      if (subscribed == 'True')
      {
        $('#subscribe-button').html('Subscribe');
        $('#subscribe-button').attr('onclick','subscribe('+"'"+username+"'"+',"False");');
        $('.subscribers-number').html(data.subscribers);
        display_messages(data.ajax_messages);
      }
      else
      {  
        $('#subscribe-button').html('Unsubscribe');
        $('#subscribe-button').attr('onclick','subscribe('+"'"+username+"'"+',"True");');
        $('.subscribers-number').html(data.subscribers);
        display_messages(data.ajax_messages);
      } 
    }  
  );
}

