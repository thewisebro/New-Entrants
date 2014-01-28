var current_tab, tabs, tabs_parent_top;
var showLoading = true;

function open_login_dialog(){
  dialog_iframe({
    name: 'login_dialog',
    title: 'Sign In',
    width: 400,
    height: 200,
    src: '/login_dialog/?next=/close_dialog/login_dialog/',
    close: function(){
      user_logged_in = true;
      $(document).trigger("login");
    }
  });
}

function logout(){
  $.get('/logout_ajax/',{
    },function(data){
      user_logged_in = false;
      $(document).trigger("logout");
  });
}

$(document).on("login", function(){
  load_pagelet("header");
  load_pagelet("sidebar");
});

$(document).on("logout", function(){
  load_pagelet("header");
  load_pagelet("sidebar");
});

$(document).on("pagelet_loaded_sidebar",function(){
  tabs = $('.tab').map(function(){return this.id.split('-')[0];});
  tabs_parent_top = $('#sidebar-tabs').position().top;
  var load = true;
  if(current_tab)
    load = false;
  current_tab = undefined;
  hashchangeCallback(load);
});

$('#loading-div')
  .hide()
  .ajaxStart(function(){
    if(showLoading)
      $(this).show();
  }).ajaxStop(function(){
    $(this).hide();
    showLoading = true;
  });


function tab_clicked(tab){
    location.hash = tab;
}

function hashchangeCallback(load){
  var hashtags = location.hash.substr(1).split('/');
  var first_hashtag = hashtags.shift();
  if(!first_hashtag)first_hashtag = tabs[0];
  if(load)
    load_app(first_hashtag,function(){
      $(document).trigger("load_app_"+first_hashtag, hashtags);
      $('.nano').nanoScroller();
    });
  if($.inArray(first_hashtag, tabs) > -1){
    var tab = first_hashtag;
    if(current_tab!=tab){
      $('#'+tab+'-tab').addClass('active-tab');
      $('#'+current_tab+'-tab').removeClass('active-tab');
    }
    var position = $('#'+tab+'-tab').position();
    if(current_tab)
      $('#tab-arrow').animate({top:position.top+tabs_parent_top},100);
    else{
      $('#tab-arrow').css({top:position.top+tabs_parent_top});
      $('#tab-arrow').show();
    }
    current_tab = tab;
  }
}

$(window).bind('hashchange', hashchangeCallback);

function get_current_app(){
  var hashtags = location.hash.substr(1).split('/');
  var first_hashtag = hashtags.shift();
  return first_hashtag;
}

function get_app_hashtags(){
  var hashtags = location.hash.substr(1).split('/');
  var first_hashtag = hashtags.shift();
  return hashtags;
}
