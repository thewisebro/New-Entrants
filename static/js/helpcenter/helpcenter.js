var responses = Array();
var responses_per_request = 20;
var more_responses = true;
var img_dp_url = '/static/images/nucleus/img_dp.png';

$(document).on("load_app_helpcenter", function(e,hash1,hash2){
  if(!user.is_authenticated){
    redirect_to_home();
    return;
  }
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

$(document).on("logout", function(){
  redirect_to_home();
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

function reply_html(reply){
  return ""+
    "<div class='reply-main'>"+
      "<img class='profile-pic-small' src='"+(reply.username == 'img'?img_dp_url:reply.user_photo)+"'/>"+
      "<div class='reply-text'>" + reply.text + "</div>"+
    "</div>"
}
function response_html(response,close_replies){
  var html = ""+
    "<div class='query-box'>"+
      "<div class='query-main'>"+
        "<input class='seen' type='checkbox' "+('resolved' in response?"onchange='checkbox_clicked(this,"+response.id+");' "+(response.resolved?"checked='checked'":""):"style='display:none;' ")+"/>"+
        "<div class='query-main-content' onclick='min_max("+response.id+");'>"+
          "<img class='profile-pic' src='"+response.user_photo+"'/>"+
          "<div class='person-name'>"+(response.user_name)+"</div>"+
          "<div class='min-max' id='min-max"+response.id+"'>"+(close_replies?"&#9660;":"&#9650;")+"</div>"+
          "<div class='posted'>"+prettyDate(response.datetime)+"</div>"+
          "<div class='posted'>"+response.response_type+"</div>"+
          "<div class='query-app-name'>"+
            (response.app in channeli_apps?"<a target='_blank' href='"+channeli_apps[response.app]['url']+"'>"+channeli_apps[response.app]['name']+"</a>":response.app)+
          "</div>"+
          "<div class='query-text'>"+response.text+"</div>"+
        "</div>"+
      "</div>"+
      "<div id='replies"+response.id+"' class='replies'"+(close_replies?" style='display:none'":"")+">"+
        "<div id='main-replies"+response.id+"'>"
  for(var i=0;i<response.replies.length;i++)
    html += reply_html(response.replies[i]);

  html += ""+
        "</div>"+
        (response.username!='anonymous' || response.replies.length==0
          ?"<div class='write-reply'>"+
            "<img class='profile-pic-small' src='"+(user_in_img?img_dp_url:user.photo)+"'/>"+
              "<form action='' method='POST' onsubmit='give_reply(\""+response.id+"\");return false;'>"+
                "<textarea id='reply"+response.id+"' name='reply' class='reply-box' type='text'></textarea>"+
                "<input class='input-button' type='submit' name='submit' style='margin-top:1px;margin-left:10px;' value='"+
                  (response.username!='anonymous' ? 'Reply' : 'Email') +"'/>"+
              "</form>"+
          "</div>"
          :"")+
      "</div>"+
    "</div>"

  return html;
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
 //$('#responses').pickify_users();
 if(more_responses && $('#see-more-responses').length==0){
   $('#content-down').append("<div id='see-more-responses' class='see-more'><span class='button2' onclick='see_more_responses();'>See More</span></div>");
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
