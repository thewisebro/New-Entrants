var settings_tabs = [
  {name: 'profile', show: 'Edit profile'},
  {name: 'password', show: 'Change password'},
  {name: 'email', show: 'Email notifications'},
  {name: 'sessions', show: 'Manage sessions'},
  {name: 'email_auth', show: 'Email verification'}
//  {name: 'forgot_password', show: 'Forgot Password'}
];

$(document).on("load_app_settings", function(e, hash1, hash2){
  if(hash1 == 'password_reset'){
    console.log("abc");
    nucleus.redirect_to_home();
    dialog_iframe({
      name:'pass_reset',
      title:'Reset Password',
      width:450,
      height:180,
      close: nucleus.redirect_to_home(),
      src:'/settings/password_reset/'+hash2
    });
    }
  else{
    if(!user.is_authenticated){
      nucleus.redirect_to_home();
      return;
    }
    nucleus.make_tabs_inactive();
    $('#right-column .content').html('');
    if(hash1 === undefined)
      nucleus.redirect_to_hash('settings/profile');
    if(settings_tabs.some(function(tab){return tab.name==hash1;}))
      load_settings_tab(hash1);}
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
  var pagelet_url = nucleus.get_app_hashtags().join('/');
  $('#content').html("<div class='app-heading'>Settings: "+
      settings_tabs.filter(function(a){return a.name==tab;})[0].show + "</div><div "+
      "id='content-pagelet' class='pagelet' pagelet-url='/settings/"+pagelet_url+"'></div>");
  $('#right-column .content').html(settings_links_html(tab));
  $('.settings-label').removeClass('active-label');
  $('#settings-label-'+tab).addClass('active-label');
  load_pagelet('content-pagelet');
}

function settings_label_clicked(tab){
  location.hash = 'settings/'+tab;
}
