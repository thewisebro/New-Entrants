function dialog_iframe(data){
  var $dialog;
  try {
    $dialog = eval(data.name);
  }catch(e){}

  if(!$dialog){
    var height,margin;
    if($(window).height()>(data.height+100)){
      height = data.height;
      margin = ($(window).height()-height)/2;
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
          "<iframe id='"+data.name+"-iframe' src='"+data.src+"' width='100%' height='98%' frameborder=0></iframe>"
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
  eval(data.name+'=$dialog;')
}

function open_login_dialog(){
  dialog_iframe({
    name: 'login_dialog',
    title: 'Sign In',
    width: 400,
    height: 250,
    src: '/login_dialog/?next=/close_dialog/login_dialog/',
    close: function(){
      user_logged_in = true;
      $(document).trigger("login");
    }
  });
}

function close_dialog(dialog_name){
  eval(dialog_name).dialog('close');
}

function load_pagelets(dom_elem){
  $(dom_elem).find('.pagelet').each(function(){
    var pagelet_name = $(this).attr('id');
    $(this).load($(this).attr('pagelet-url'),function(){
      $(document).trigger("pagelet_loaded_"+pagelet_name);
      load_pagelets(this);
    });
  });
};

function load_pagelet(pagelet_name){
  var $elem = $('.pagelet#'+pagelet_name);
  $elem.load($elem.attr('pagelet-url'),function(){
    $(document).trigger("pagelet_loaded_"+pagelet_name);
    load_pagelets($elem);
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
      user_logged_in = false;
      $(document).trigger("logout");
  });
}
