var groups = null;

$(document).on("load_app_groups", function(e, hash1, hash2){
  $('#right-column .content').html('');
  //$('#container').addClass('large-width-content');
  if(!groups){
    $.get("groups/get_groups/", function(data){
        groups = data;
        show_groups(hash1);
    });
  }
  else
    show_groups(hash1);
  show_default_right_column();
  load_groups_tab(hash1, hash2);
});

function show_groups(hash1){
  console.log(hash1);
  if(!hash1){
    $('#content').html(Handlebars.groups_templates.groups_list(groups));
    $('#content').pickify_users();
  }
}


$(document).on("unload_app_groups", function(e){
  $('#container').removeClass('large-width-content');
  //$('#right-column .content').empty();
});

function groups_on_login_and_logout(){
  if(nucleus.get_current_app() == 'groups'){
    var hashtags = nucleus.get_app_hashtags();
    $(document).trigger("load_app_groups", hashtags);
  }
}

$(document).on("login", groups_on_login_and_logout);
$(document).on("logout", groups_on_login_and_logout);

function load_groups_tab(hash1, hash2){
  if(hash1 && !hash2)
  {
    $('#content').html("<div "+
      "id='content-pagelet' class='pagelet' pagelet-url='/groups/"+hash1+"/'></div>");
  }
  else if(hash1 && hash2)
  {
    $('#content').html("<div "+
      "id='content-pagelet' class='pagelet' pagelet-url='/groups/"+hash1+"/" + hash2 + "/'></div>");
  }
  //$('#right-column .content').html(settings_links_html(tab));
  //$('.settings-label').removeClass('active-label');
  //$('#settings-label-'+tab).addClass('active-label');
  load_pagelet('content-pagelet', function(){
    $('#groups-content').pickify_users();
  });
}

