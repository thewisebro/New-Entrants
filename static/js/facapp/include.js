function dialog_iframe(data){
  var $dialog;
  try{
    $dialog = eval(data.name);
  }catch(e){}  
  if(!$dialog){    
    var height,margin;
    if($(window).height()>(data.height+100))
    { height = data.height;
      margin = ($(window).height()-height)/2;
    }
    else
    { margin = 50;
      height = $(window).height()-2*margin;
    } 
    $('body').append("<div id='"+data.name+"-div'></div>");
    $dialog = $('#'+data.name+'-div')
      .html('<p>Loading...</p>')
      .dialog({
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
        }, 
        open: function(event, ui){ 
          $('#'+data.name+'-div').html(""+
            "<iframe id='"+data.name+"-iframe' src='"+data.src+"' width='100%' height='98%' frameborder=0></iframe>"
          );
        }
    });
  }
  $('.dialog-class').css({position:'fixed'});
  $dialog.dialog('open');
  eval(data.name+'=$dialog;')
}

function display_messages(messages){
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

function html_name(user){
  return "<span class='user-span' data-username='"+user.username+"' data-info='"+user.info+"' data-photo='"+user.photo+"'>"+user.name+"</span>";
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
  
            $('body').append("<div class='pickdiv'></div>");
  $.fn.pickify_users = function(){

    this.find('.user-span').live("mouseover",function(){
      mouse_out_of_span = false;
      setTimeout(function(elem){
        if($(elem).is(':hover') && last_user_span != elem){
          last_user_span = elem;
          if($('.pickdiv').length==0){
         //   $('body').append("<div class='pickdiv'></div>");
          }
          $('.pickdiv').show();
          $('.pickdiv').css({
            top:window.mouseYPos-95,
            left:window.mouseXPos-10
          }).html(
            "<div class='name-info-div'>"+
              "<div class='name-div'>"+($(elem).data().shortname?$(elem).data().shortname:$(elem).html())+"</div>"+
              "<div class='info-div'>"+$(elem).data().info+"</div>"+
            "</div>"+  
            "<img "+($(elem).data().photo?"src='"+$(elem).data().photo+"'":"src='/photo/"+$(elem).attr('data-username')+"/'")+" style=''/>"
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

    this.find('.user-span').live("mouseout",function(){
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

