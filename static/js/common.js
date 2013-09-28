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

function close_dialog(dialog_name){
  eval(dialog_name).dialog('close');
}

function load_pagelets(dom_elem){
  $(dom_elem).find('.pagelet').each(function(){
    $(this).load($(this).attr('pagelet-url'),function(){
      load_pagelets(this);
    });
  });
};

function load_pagelet(pagelet_name){
  var $elem = $('.pagelet#'+pagelet_name);
  $elem.load($elem.attr('pagelet-url'),function(){
    load_pagelets($elem);
  });
}

$(document).ready(function(){
  load_pagelets(document);
});
