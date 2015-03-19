$(document).on("load_app_groups", function(e, hash1, hash2){
  if(!user.is_authenticated){
    nucleus.redirect_to_home();
    return;
  }
  //nucleus.make_tabs_inactive();
  $('#right-column .content').html('');
  //$('#container').addClass('large-width-content');
  if(hash1 === undefined)
    nucleus.redirect_to_home();
  load_groups_tab(hash1, hash2);
});

$(document).on("unload_app_groups", function(e){
  $('#container').removeClass('large-width-content');
  nucleus.make_tabs_active();
  $('#right-column .content').empty();
});

$(document).on("logout", function(){
  if(nucleus.get_current_app() == 'groups')
    nucleus.redirect_to_home();
});

function load_groups_tab(hash1, hash2){
  if(hash2 === undefined)
  {
    $('#content').html("<div "+
      "id='content-pagelet' class='pagelet' pagelet-url='/groups/"+hash1+"'></div>");
  }
  else
  {
    $('#content').html("<div "+
      "id='content-pagelet' class='pagelet' pagelet-url='/groups/"+hash1+"/" + hash2 + "/'></div>");
  }
  //$('#right-column .content').html(settings_links_html(tab));
  //$('.settings-label').removeClass('active-label');
  //$('#settings-label-'+tab).addClass('active-label');
  load_pagelet('content-pagelet');
}

