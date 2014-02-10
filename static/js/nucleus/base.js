var current_tab, tabs, tabs_parent_top;
var showLoading = true;

$(document).on("login", function(){
  load_pagelet("header");
  load_pagelet("sidebar");
});

$(document).on("pagelet_loaded_sidebar",function(){
  tabs = $('.tab').map(function(){return this.id.split('-')[0];});
  tabs_parent_top = $('#sidebar-tabs').position().top;
  current_tab = undefined;
  hashchangeCallback();
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

function hashchangeCallback(){
  var hashtags = location.hash.substr(1).split('/');
  var first_hashtag = hashtags.shift();
  if(!first_hashtag)first_hashtag = tabs[0];
  load_app(first_hashtag,function(){
    $(document).trigger("load_app_"+first_hashtag, hashtags);
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
