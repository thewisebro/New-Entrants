(function(){

  namespace("nucleus",
      get_current_app, get_app_hashtags,
      redirect_to_hash, redirect_to_home, tab_clicked,
      make_tabs_inactive, make_tabs_active
  );

  var tabs, tabs_parent_top;
  var showLoading = true;
  var previous_hashtags = null;
  var previous_app = null;
  var account_navigation_open = false;

  $(document).ready(function(){
    $('body').click(function(){
      if(account_navigation_open)
        $('#account-navigation').hide();
        account_navigation_open = false;
    });
  });


  $(document).on("login", function(){
    load_pagelet("header_sidebar");
    $(window).scrollTop(0);
  });

  $(document).on("logout", function(){
    load_pagelet("header_sidebar");
    $(window).scrollTop(0);
  });

  function attach_bindings_on_header_sidebar(){
    $('#user-account').click(function(e){
      if(!account_navigation_open){
        $('#account-navigation').show();
        account_navigation_open = true;
        e.stopPropagation();
      }
    });
    $('#notifications-count').click(function(){
      location.hash = 'notifications';
    });
  }

  $(document).on("pagelet_loaded_header_sidebar",function(){
    attach_bindings_on_header_sidebar();
    tabs = $('.tab').map(function(){return this.id.split('-')[0];});
    tabs_parent_top = $('#sidebar-tabs').position().top;
    var load = true;
    if(typeof current_tab === 'undefined')
      current_tab = undefined;
    else if(current_tab)
      load = false;
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

  function make_tabs_inactive(){
    current_tab = null;
    $('.active-tab').removeClass('active-tab');
    $('#tab-arrow').hide();
  }

  function make_tabs_active(){
    $('#tab-arrow').show();
  }

  function hashchangeCallback(load){
    var hashtags = location.hash.substr(1).split('/');
    var first_hashtag = hashtags.shift();
    if(!first_hashtag)first_hashtag = tabs[0];
    if(load)
      load_app(first_hashtag, function(){
        if(previous_app !== first_hashtag){
          $(document).trigger("unload_app_"+previous_app, [first_hashtag,
            hashtags, previous_hashtags]);
          $(window).scrollTop(0);
        }
        document.title = 'Channel i - '+first_hashtag.toProperCase();
        $(document).trigger("load_app_"+first_hashtag, hashtags);
        previous_app = first_hashtag;
        previous_hashtags = hashtags;
        $('.nano').nanoScroller();
      });
    if($.inArray(first_hashtag, tabs) > -1){
      var tab = first_hashtag;
      $('#'+tab+'-tab').addClass('active-tab');
      if(current_tab!=tab){
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
    if(!first_hashtag)first_hashtag = tabs[0];
    return first_hashtag;
  }

  function get_app_hashtags(){
    var hashtags = location.hash.substr(1).split('/');
    var first_hashtag = hashtags.shift();
    return hashtags;
  }

  function redirect_to_home(){
    history.replaceState({},'home','/');
    hashchangeCallback(true);
  }

  function redirect_to_hash(hash){
    history.replaceState({},hash,'/#'+hash);
    hashchangeCallback(true);
  }

})();
