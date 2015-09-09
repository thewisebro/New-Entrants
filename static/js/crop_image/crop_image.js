var uname;

function upload_image(unique_name, id){
  uname = unique_name;
  dialog_iframe({
    name: 'upload_image_dialog',
    title: 'Upload Image',
    width: 700,
    height: 500,
    src: '/crop_image/upload_image/' + unique_name + '/' + id + '/'
  });
}

function cropping_done(image_url){
  close_dialog('upload_image_dialog');
  $('#'+uname+'-img').attr('src',image_url);
  if (uname == 'buyandsell_pic')
  {
    window.top.location = "/buyandsell/buy";
  }
}

function setup_jcrop(){
  jQuery(function($){
    var jcrop_api, boundx, boundy;

    $('#target').Jcrop({
      onChange: updatePreview,
      onSelect: updatePreview,
      aspectRatio: crop_image_width/crop_image_height,
      bgColor: 'white',
      bgFade: true,
      bgOpacity: 0.5,
      setSelect: [200-crop_image_width/2,100-crop_image_height/2,
                  200+crop_image_width/2, 100+crop_image_height/2],
    },function(){
      var bounds = this.getBounds();
      boundx = bounds[0];
      boundy = bounds[1];
      jcrop_api = this;

      $('#preview').css({
        width: Math.round(1 * boundx) + 'px',
        height: Math.round(1 * boundy) + 'px',
        marginLeft: '-' + Math.round(1*150) + 'px',
        marginTop: '-' + Math.round(1*50) + 'px'
      });

      jcrop_api.ui.selection.addClass('jcrop-selection');
     });

    function updatePreview(c){
      if (parseInt(c.w) > 0){
        var rx = crop_image_width / c.w;
        var ry = crop_image_height / c.h;
        $('#preview').css({
           width: Math.round(rx * boundx) + 'px',
           height: Math.round(ry * boundy) + 'px',
           marginLeft: '-' + Math.round(rx * c.x) + 'px',
           marginTop: '-' + Math.round(ry * c.y) + 'px'
        });
        $('#x').val(c.x);
        $('#y').val(c.y);
        $('#w').val(c.w);
        $('#h').val(c.h);
      }
    };
  });
}
