var settings_tabs = [
  {name: 'profile', show: 'Edit profile'},
  {name: 'password', show: 'Change password'},
  {name: 'email', show: 'Email notifications'},
  {name: 'sessions', show: 'Manage sessions'}
];

$(document).on("load_app_settings", function(e, hash1){
  if(!user.is_authenticated){
    nucleus.redirect_to_home();
    return;
  }
  nucleus.make_tabs_inactive();
  $('#right-column .content').html('');
  if(hash1 === undefined)
    nucleus.redirect_to_hash('settings/profile');
  if(settings_tabs.some(function(tab){return tab.name==hash1;}))
    load_settings_tab(hash1);
});

$(document).on("unload_app_settings", function(e){
  $('#container').removeClass('large-width-content');
  nucleus.make_tabs_active();
  $('#right-column .content').empty();
});

$(document).on("logout", function(){
  if(nucleus.get_current_app() == 'settings')
    nucleus.redirect_to_home();
});

function settings_links_html(current_tab){
  return Handlebars.utilities_templates.links_div({
    settings_tabs: settings_tabs,
  });
}

function load_settings_tab(tab){
  $('#content').html("<div class='app-heading'>Settings: "+
      settings_tabs.filter(function(a){return a.name==tab;})[0].show + "</div><div "+
      "id='content-pagelet' class='pagelet' pagelet-url='/settings/"+tab+"/'></div>");
  $('#right-column .content').html(settings_links_html(tab));
  $('.settings-label').removeClass('active-label');
  $('#settings-label-'+tab).addClass('active-label');
  load_pagelet('content-pagelet');
}

function settings_label_clicked(tab){
  location.hash = 'settings/'+tab;
}
