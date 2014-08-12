var settings_tabs = ['profile', 'password', 'email', 'sessions'];

$(document).on("load_app_settings", function(e, hash1){
  if(!user.is_authenticated){
    redirect_to_home();
    return;
  }
  $('.active-tab').removeClass('active-tab');
  current_tab = null;
  $('#tab-arrow').hide();
  $('#right-column .content').html('');
  if(hash1 === undefined)
    redirect_to_hash('settings/profile');
  if($.inArray(hash1, settings_tabs)>-1)
    load_settings_tab(hash1);
});

$(document).on("unload_app_helpcenter", function(e){
  $('#container').removeClass('large-width-content');
  $('#tab-arrow').show();
});

$(document).on("logout", function(){
  if(get_current_app() == 'settings')
    redirect_to_home();
});

function load_settings_tab(hash1){
  $('#content').html("<div class='app-heading'>Account Settings</div><div "+
      "id='content-pagelet' class='pagelet' pagelet-url='/settings/"+hash1+"/'></div>");
  load_pagelet('content-pagelet');
}
