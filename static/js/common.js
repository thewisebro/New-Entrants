function dialog_iframe(data){
  var $dialog;
  try {
    $dialog = eval(data.name);
  }catch(e){}

  if(!$dialog){
    var height,margin;
    var related_window_height = $(window).height();
    related_window_height -= (1-data.height/related_window_height)*150;
    if(related_window_height>(data.height+100)){
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
  eval(data.name+'=$dialog;');
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
      user = {
        is_authenticated: false
      };
      $(document).trigger("logout");
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
