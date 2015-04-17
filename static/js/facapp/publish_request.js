function display_messages(messages){
  if(messages.length > 0){
    var message = messages.shift(1);
    $('#messages-div').html("<span class='message-span'>"+message.message+"</span>");
    setTimeout(function(){
        $('#messages-div').html('');
        setTimeout(function(){
            display_messages(messages);
          },500  
        );
      },4000
    );
  } 
  else
    $('#messages-div').html('');
}
function send_request(username)
{
  url = "/facapp/publish/"
  $.post(url,
      {
      },
    function(data)
    {
      display_messages(data.ajax_messages);
    }
  );
}
