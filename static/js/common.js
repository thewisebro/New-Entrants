var loaded_scripts = [];
var loaded_styles = [];
var current_dialog;

$(document).on('ready', function(){
  var scripts = $('script');
  for(var i=0; i<scripts.length; i++){
    var script = scripts[i];
    var src = script.getAttribute('src');
    if(src)
      loaded_scripts.push(src);
  }
  var styles = $('link[rel=stylesheet]');
  for(i=0; i<styles.length; i++){
    var style = styles[i];
    var href = style.getAttribute('href');
    if(href)
      loaded_styles.push(href);
  }
});

function load_script(script){
  if($.inArray(script, loaded_scripts) == -1){
    loaded_scripts.push(script);
    return $.cachedScript(script);
  }
}

function load_css(href){
  if($.inArray(href, loaded_styles) == -1){
    $('head').append('<link rel="stylesheet" href="'+href+'" type="text/css" />');
    loaded_styles.push(href);
  }
}

function load_scripts_in_pipe(scripts, callback){
  var deferred = new $.Deferred(), pipe = deferred;

  $.each(scripts , function(i, val){
    pipe = pipe.pipe(function(){
      return load_script(val);
    });
  });

  if(callback)
    pipe = pipe.pipe(callback);
  deferred.resolve();
}

String.prototype.toProperCase = function() {
    return this.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
};

function dialog_iframe(data){
  var $dialog;
  try {
    $dialog = eval(data.name);
  }catch(e){}

  if(!$dialog){
    var height,margin;
    var related_window_height = $(window).height();
    related_window_height -= (1-data.height/related_window_height)*150;
    if(related_window_height > data.height){
      height = data.height;
      margin = (related_window_height-height)/2;
    }
    else{
      margin = 50;
      height = $(window).height()-2*margin;
    }
    $('body').append("<div id='"+data.name+"-div'></div>");
    dialog_options = {
      autoOpen: false,
      dialogClass: 'dialog-class',
      title: data.title,
      position: ['center',margin],
      width: data.width,
      height: height,
      draggable: false,
      resizable: false,
      sticky: true,
      close: function(event, ui){
        eval('delete '+data.name);
        $('#'+data.name+'-div').remove();
      },
      open: function(event, ui){
        $('#'+data.name+'-div').html(""+
          "<iframe id='"+data.name+"-iframe' src='"+data.src+
          "' width='100%' height='98%' frameborder=0></iframe>"
        );
      }
    };
    if('close' in data)
      dialog_options.beforeClose = data.close;
    $dialog = $('#'+data.name+'-div')
                .html('<p>Loading...</p>')
                .dialog(dialog_options);
  }
  $('.dialog-class').css({position:'fixed'});
  $dialog.dialog('open');
  eval(data.name+'=$dialog;');
  current_dialog = $dialog;
}

function open_login_dialog(){
  dialog_iframe({
    name: 'login_dialog',
    title: 'Sign In',
    width: 410,
    height: 260,
    src: '/login_dialog/?next=/close_dialog/login_dialog/',
    close: function(){
      if(typeof user === "undefined") {
        user = {
          is_authenticated: false
        };
      }
      if(user.is_authenticated) {
        $(document).trigger("login");
      }
    }
  });
}

function close_dialog(dialog_name){
  eval(dialog_name).dialog('close');
  current_dialog = null;
}

function check_user_data(is_authenticated, username){
  if(!(is_authenticated === true || is_authenticated === false))
    return;
  if(user.is_authenticated != is_authenticated ||
      (user.is_authenticated && user.username != username)){
    if(is_authenticated){
      user = {
        is_authenticated: true,
        username: username
      };
    }
    else{
      user = {
        is_authenticated: false
      };
    }
    if(current_dialog){
      try{
        current_dialog.dialog('close');
      } catch(e){}
    }
    console.log('is_authenticated: '+is_authenticated);
    console.log('username: '+username);
    if(is_authenticated)
      $(document).trigger('login');
    else
      $(document).trigger('logout');
  }
}

function load_pagelets(dom_elem){
  $(dom_elem).find('.pagelet').each(function(){
    var pagelet_name = $(this).attr('id');
    $(this).load($(this).attr('pagelet-url'),function(){
      $(document).trigger("pagelet_loaded_"+pagelet_name);
      load_pagelets(this);
    });
  });
}

function fill_data_in_pagelet(pagelet_name, html){
  var $elem = $('.pagelet#'+pagelet_name);
  var wrapped_html = $('<div>'+html+'</div>');
  var styles = wrapped_html.find('link[rel=stylesheet]');
  var scripts = wrapped_html.find('script[src]');
  var messages = wrapped_html.find('messages');
  var userdata = wrapped_html.find('userdata');
  for(var i=0; i<styles.length; i++){
    var style = styles[i];
    var href = style.getAttribute('href');
    if(href) load_css(href);
  }
  styles.remove();
  scripts.remove();
  messages.remove();
  userdata.remove();
  html = wrapped_html.html();
  $elem.html(html);
  display_messages(eval($(messages).attr('data')));
  check_user_data(
      eval($(userdata).attr('is_authenticated')),
      $(userdata).attr('username')
  );
  var script_src_list = [];
  for(i=0; i<scripts.length; i++){
    var script = scripts[i];
    var src = script.getAttribute('src');
    if(src) script_src_list.push(src);
  }
  load_scripts_in_pipe(script_src_list, function(){
    if(typeof setup_form != "undefined")
      setup_form();
  });
  $(document).trigger("pagelet_loaded_"+pagelet_name);
  ajaxform_success = function(data){
    fill_data_in_pagelet(pagelet_name, data);
  };
  forms = $elem.find('form');
  for(i=0; i<forms.length; i++){
    var $form = $(forms[i]);
    if($form.attr('action') === '')
      $form.attr('action',$elem.attr('pagelet-url'));
    $form.ajaxForm({
      success: ajaxform_success
    });
  }
  load_pagelets($elem);
}

function load_pagelet(pagelet_name, callback){
  var $elem = $('.pagelet#'+pagelet_name);
  $.ajax({
    type: "GET",
    url: $elem.attr('pagelet-url')
  }).done(function(html){
    fill_data_in_pagelet(pagelet_name, html);
    if(callback)callback();
  });
}

$(document).ready(function(){
  load_pagelets(document);
});

jQuery.cachedScript = function(url, options){
  options = $.extend(options || {},{
    dataType: "script",
    cache: true,
    url: url
  });
  return jQuery.ajax(options);
};

function display_messages(messages){
  if(!messages)return;
  if(messages.length > 0){
    var message = messages.shift(1);
    $('#messages-div').html("<span class='"+message.extra_tags+" message-span'>"+message.message+"</span>");
    setTimeout(function(){
        $('#messages-div').html('');
        setTimeout(function(){
            display_messages(messages);
          },500
        );
      },4000
    );
  }
  else
    $('#messages-div').html('');
}

function logout(){
  $.get('/logout_ajax/',{
    },function(data){
      user = {
        is_authenticated: false
      };
      $(document).trigger("logout");
  });
}

function take_feedback(){
  dialog_iframe({
    name:'feedback_dialog',
    title:'Feedback',
    width:600,
    height:360,
    src:'/helpcenter/feedback/'
  });
}

function sell_form(){
 if(typeof dialog_options != "undefined")
  {
    dialog_options.close();
  }
 dialog_iframe({
    name:'sell_form_dialog',
    title:'SellForm',
    width:600,
    height:360,
    src:'/buyandsell/sell/'
  });
}

function request_form(){
if(typeof dialog_options != "undefined")
  {
    dialog_options.close();
  }
 dialog_iframe({
    name:'request_form_dialog',
    title:'RequestForm',
    width:600,
    height:360,
    src:'/buyandsell/requestitem/'
  });
}
function sell_details(pk){
if(typeof dialog_options != "undefined")
  {
    dialog_options.close();
  }
 dialog_iframe({
    name:'sell_detail_dialog',
    title:'SellItemDetails',
    width:600,
    height:360,
    src:'/buyandsell/sell_details/'+pk+'/'
  });
}

function request_details(pk){
if(typeof dialog_options != "undefined")
  {
    dialog_options.close();
  }
 dialog_iframe({
    name:'request_detail_dialog',
    title:'RequestItemDetails',
    width:600,
    height:360,
    src:'/buyandsell/request_details/'+pk+'/'
  });
}
function edit_sell(pk){
if(typeof dialog_options != "undefined")
  {
    dialog_options.close();
  }
 dialog_iframe({
    name:'edit_sell_dialog',
    title:'EditSellItem',
    width:600,
    height:360,
    src:'/buyandsell/edit/sell/'+pk+'/'
  });
}
function edit_request(pk){
if(typeof dialog_options != "undefined")
  {
    dialog_options.close();
  }
 dialog_iframe({
    name:'edit_request_dialog',
    title:'EditRequestItem',
    width:600,
    height:360,
    src:'/buyandsell/edit/request/'+pk+'/'
  });
}
function submit_report(object_pk, content_type_pk){
  $.get('/moderation/report_info/',{
    content_type_pk: content_type_pk,
    object_pk: object_pk
  },function(data){
    if(data.open_dialog){
      dialog_iframe({
        name:'report_dialog',
        title:'Report Item',
        width:280,
        height:280,
        src:'/moderation/submit_report/?content_type_pk='+
            content_type_pk+'&object_pk='+object_pk
      });
    }
  });
}

function user_html_name(user){
  return "<span class='user-span' data-username='"+user.username+
          "' data-info='"+user.info+"' data-photo='"+user.photo+"'>"+
          user.name+"</span>";
}

$(document).ready(function(){
  $(document).mousemove(function(e){
    window.mouseXPos = e.pageX;
    window.mouseYPos = e.pageY;
  });
});

(function($){
  var mouse_out_of_pickdiv = true;
  var mouse_out_of_span = true;
  var last_user_span = null;

  $.fn.pickify_users = function(){
    this.find('.user-span').mouseover(function(){
      mouse_out_of_span = false;
      setTimeout(function(elem){
        if($(elem).is(':hover') && last_user_span != elem){
          last_user_span = elem;
          if($('.pickdiv').length === 0){
            $('body').append("<div class='pickdiv'></div>");
          }
          $('.pickdiv').show();
          $('.pickdiv').css({
            top:window.mouseYPos-95,
            left:window.mouseXPos-10
          }).html(
            "<div class='name-info-div'>"+
              "<div class='name-div'>"+($(elem).data().shortname?
                $(elem).data().shortname:$(elem).html())+"</div>"+
              "<div class='info-div'>"+$(elem).data().info+"</div>"+
            "</div>"+
            "<img "+($(elem).data().photo?"src='"+$(elem).data().photo+"'":"src='/photo/"+
              $(elem).attr('data-username')+"/'")+" style=''/>"
          );
          $('.pickdiv').mouseout(function(){
            mouse_out_of_pickdiv = true;
            setTimeout(function(){
              if(!$(elem).is(':hover') && mouse_out_of_pickdiv && mouse_out_of_span){
                $('.pickdiv').hide();
                last_user_span = null;
              }
            },300);
          });
          $('.pickdiv').mouseover(function(){
            mouse_out_of_pickdiv = false;
          });
        }
      },300,this);
    });
    this.find('.user-span').mouseout(function(){
      mouse_out_of_span = true;
      setTimeout(function(elem){
        if(!$(elem).is(':hover') && mouse_out_of_pickdiv && mouse_out_of_span){
          $('.pickdiv').hide();
          last_user_span = null;
        }
      },300,this);
    });
  };
})(jQuery);
