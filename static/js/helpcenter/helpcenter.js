var responses = Array();
var responses_per_request = 20;
var more_responses = true;
var img_dp_url = '/static/images/nucleus/img_dp.png';

$(document).on("load_app_helpcenter", function(e,hash1,hash2){
  if(!user.is_authenticated){
    nucleus.redirect_to_home();
    return;
  }
  nucleus.make_tabs_inactive();
  $('#right-column .content').html('');
  $('#content').html('');
  $('#container').addClass('large-width-content');
  $('#content').load('/helpcenter/pagelet_index/',function(){
    if(hash1=='exact'){
      $('#give_response').hide();
      $('.helpcenter-header').hide();
      update_responses('exact',hash2);
    }
    else
      update_responses('first');
  });
});

$(document).on("unload_app_helpcenter", function(e){
  $('#container').removeClass('large-width-content');
  nucleus.make_tabs_active();
});

$(document).on("logout", function(){
  if(nucleus.get_current_app() == 'helpcenter')
    nucleus.redirect_to_home();
});

function update_responses(action,id){
  if(!id)id = null;
  if(action == 'next')
    id = responses[responses.length-1].id;
  $.get("/helpcenter/fetch",
    {'action' : action,
     'id' : id,
     'number' : responses_per_request,
     'response_type':'help'
    },
    function(data){
      if(action != 'previous'){
        responses = responses.concat(data.responses);
        more_responses = data.more?true:false;
        display_add_responses('bottom',data.responses,(action != 'exact') ? true : false);
      }
    }
  );
}

function reply_html(reply) {
  return Handlebars.helpcenter_templates.reply({
    reply: reply,
    profile_pic_url: (reply.username == 'img') ? img_dp_url : reply.user_photo
  });
}

function response_html(response, close_replies) {
  response.pretty_datetime = prettyDate(response.datetime);
  for(var i=0; i<response.replies.length; i++){
    var reply = response.replies[i];
    reply.html = reply_html(reply);
  }
  if(response.app in channeli_apps){
    response.app_url = channeli_apps[response.app].url;
    response.app_name = channeli_apps[response.app].name;
  }
  var context = {
    response: response,
    close_replies: close_replies,
    channeli_apps: channeli_apps,
    reply_pic_url: (user_in_img ? img_dp_url : user.photo)
  };
  return Handlebars.helpcenter_templates.response(context);
}

function display_add_responses(position,responses,close_replies){
 for(var i=0;i<responses.length;i++){
   try{
     if(position == 'bottom')
       $('#responses').append(response_html(responses[i],close_replies));
     else if(position == 'top')
       $('#responses').prepend(response_html(responses[i],close_replies));
   }
   catch(e){
     console.log(e);
   }
 }
 $('#responses').pickify_users();
 if(more_responses && $('#see-more-responses').length === 0){
   $('#content').append(Handlebars.helpcenter_templates.see_more());
 }
 if(!more_responses && $('#see-more-responses').length==1){
  $('#see-more-responses').css('display','none');
 }
}

function see_more_responses(){
  update_responses('next');
}

function give_response(){
  $.post("/helpcenter/give_response",
    {'text':$('#id_text').val(),
     'app':$('#id_app').val(),
     'response_type':'help'
    },
    function(data){
      var response = data.response;
      if(response){
        $('#id_text').val('');
        $('#id_app').val('');
        responses = [response].concat(responses);
        display_add_responses('top',[response]);
      }
    }
  );
}

function give_reply(response_id){
  $.post("/helpcenter/give_reply",
    {'text':$('#reply'+response_id).val(),
     'response_id':response_id
    },
    function(data){
      if(data.reply){
        $('#reply'+response_id).val('');
        $('#main-replies'+response_id).append(reply_html(data.reply));
        for(var i=0;i<responses.length;i++)
          if(responses[i].id == response_id)
          { var response = responses[i];
            response.replies.push(data.reply);
            if(response.username == 'anonymous')
              $('#replies'+response_id).find('.write-reply').hide();
            break;
          }
      }
    }
  );
}

function checkbox_clicked(checkbox,response_id){
  $.post("/helpcenter/set_resolved",
    {'response_id':response_id,
     'value':checkbox.checked ? 1 : 0
    },
    function(data){
    }
  );
}

function min_max(response_id){
  $("#replies"+response_id).slideToggle('fast',function(){
    $("#min-max"+response_id).html($("#replies"+response_id).css('display') == 'none' ? "&#9660;" : "&#9650;");
  });
}
