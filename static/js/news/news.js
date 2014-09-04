var label_clicked = function(category) {
  switch(category) {
    case 'All': location.hash = "news/"; break;
    case 'National': location.hash = "news/national/"; break;
    case 'International': location.hash = "news/international/"; break;
    case 'Sports': location.hash = "news/sports/"; break;
    case 'Entertainment': location.hash = "news/entertainment/"; break;
    case 'Technology': location.hash = "news/technology/"; break;
    case 'Education': location.hash = "news/education/"; break;
    case 'Health': location.hash = "news/health/"; break;
    default: break;
  }
}

if(!Array.prototype.indexOf) {
  Array.prototype.indexOf = function(item) {
    for(var i = 0; i < this.length; i++) {
      if(this[i] === item) {
        return i;
      }
    }
    return -1;
  };
}

var channel_arr = new Array(); // Contains channels names
var channel_arr_lc = new Array(); // Contains channel names in lowercase
var current_selected_source = ""; // Tracks the current source

$(document).on('load_app_news', function(){
  if(!user.is_authenticated){
    nucleus.redirect_to_home();
    return;
  }

  var args = arguments;

  $('#global_search_bar').autocomplete({
    source : function(request, response) {
      $.get('/news/search/?q='+$("#global_search_bar").val(), function(res){
        console.log(res);
        response( $.map(res.suggestions, function(item){
          return {
            label: item.title,
            value: item.title,
            id: item.id
          }
        }));
       });
    },
    minLength: 2,
    select: function(event, ui){
      location.hash = 'news/item/'+ui.item.id+'/';
      $("#global_search_bar").val('');
      return false;
    }
  });


  $.get('/news/channels_list/', {}, function(res){
   if(res.msg == "NOUSER") { location.hash = 'news/'; return;}
   channel_arr = res.channels;
   console.log(channel_arr);
   var content = '<div id="news_cat">'+
      '<div id="labels news-labels">'+
        '<div id="labels-body">'+
          '<div class="label active-label" onclick=label_clicked("All");>'+
            '<div class="label-name">All</div>'+
          '</div>';
   for(var i=0; i<channel_arr.length; i++)
   {
      content += '<div class="label" onclick=label_clicked("'+ channel_arr[i] +'");>'+
                    '<div class="label-name">'+ channel_arr[i] +'</div>'+
                 '</div>';
      channel_arr_lc[i] = (channel_arr[i]).toLowerCase();
   }
   content += '</div>'+
              '</div>'+
              '<div style="clear:both;"></div>'+
                '<div id="customize_btn">'+
                  '<div class="div-button" onclick=location.hash="news/customize/">Customize News</div>'+
                '</div>'+
              '</div>';
   $('.content').html(content);
  });

  switch (args.length)
  {
    case 1:
      if(!(args[0] === null)) {
        $.get('/news/', function(res){
          if(res.msg == "NOUSER") { location.hash = 'news/'; }
          get_home( res );
        });
      }
      break;
    case 2:
      if((!(args[0] === null) && args[1] === "")) {
        $.get('/news/', function(res){
         if(res.msg == "NOUSER") { location.hash = 'news/'; }
         get_home( res );
        });
      }
      else if((!(args[0] === null) && channel_arr_lc.indexOf(args[1]) > -1)) {
        get_by_cat( args[1] );
      }
      else if((!(args[0] === null) && args[1] === "customize")) {
        console.log("cp-1");
        customize_page();
      }
      break;
    case 3:
      if(!(args[0] === null) && channel_arr_lc.indexOf(args[1]) > -1  && args[2] === "") {
        get_by_cat( args[1] );
      }
      else if(!(args[0] === null) && args[1] === "item" && !(args[2] === "")) {
        console.log("3-2");
        $.get('/news/item/'+args[2], function(res){
          if(res.msg == "NOUSER") { location.hash = 'news/'; }
          get_item_page( res );
        });
      }
      else if((!(args[0] === null) && args[1] === "customize" && args[2] === "")) {
        console.log("cp-2");
        customize_page();
      }
      break;
    case 4:
      if(!(args[0] === null) && !(args[1] === null) && !(args[2] === null) && args[3] === "") {
        console.log("4-1");
        $.get('/news/item/'+args[2], function(res){
          if(res.msg == "NOUSER") { location.hash = 'news/'; }
          get_item_page( res );
        });
      }
    default: break;
  }

  /*
  $(window).scroll(function() {
    if($(window).scrollTop() + $(window).height() < $(document).height()-100) {
      alert("Hey I'm there!!");
    }
  });
  var ias = jQuery.ias({
    container: '#news_items_block',
    item: '.item',
    pagnation: '#pagination',
    next: '.next'
  });

  ias.extension(new IASSpinnerExtension());
  //ias.extension(new IASTriggerExtension("show more..."));
  */
});

$(document).on("logout", function(){
  if(get_current_app() == 'news')
    nucleus.redirect_to_home();
});

function get_home( res ) {
  current_selected_source = '';
  $("#content").load('/news/', function(res){
    if(res.msg == "NOUSER") { location.hash = 'news/'; }
    res = jQuery.parseJSON(res);
    var content = construct_content(res, 'News');
    $("#content").html(content);
  });
}


function construct_related_item(data) {
  console.log(data);
  var item_html = ''+
  '<div id="item_'+ data.pk +'" class="item">'+
    '<div class="item_top_content">'+
      '<div class="item_img">';
        if(!(data.image == "noimage"))
          item_html += '<img src="newsmedia/'+data.image+'">';
      item_html +=
      '</div>'+
      '<div class="news_content">';

      item_html +=
      '<div class="item_title" onclick=location.href="#news/item/'+ data.pk +'/" >'+
        '<span>'+ data.title +'</span>'+
      '</div>'+
      '<div class="item_desc">'+
        '<span style="color:#394246;">'+
          '<p>'+data.description_text+'</p>'+
        '</span>'+
      '</div>'+
      '<div class="read_more_btn">'+
        '<a href="#news/item/'+ data.pk +'">Continue reading...</a>'+
      '</div>'+
      '<div style="clear:both"></div>'+
      '</div>'+
      '<div style="clear:both"></div>'+
    '</div>'+
    '<div class="detail_tag_box">'+
      '<div class="detail_tag">'+
        '<div class="source" onclick=\'get_by_source("'+ data.source +'");\'>'+ data.source +', </div>'+
        '<div class="published_date">'+ data.article_date +'</div>'+
      '</div>'+
      '<div style="clear:both;"></div>'+
    '</div>'+
    '<div style="clear:both;"></div>'+
  '</div>';
  return item_html
}

function get_item_page( res ) {
    var main = res.main;
    var related = res.related
    current_selected_source = '';

    var item_page_html =
      '<div id="news-header">'+
        '<div id="news_heading">'+ main.channel +'</div>'+
        '<div id="news_home">'+
          '<div class="button2" onclick="location.hash=\'news\'">'+
            'Home'+
          '</div>'+
        '</div>'+
        '<div style="clear:both;"></div>'+
      '</div>'+
      '<div style="clear:both;"></div>'+
      '<div id="news_item_'+ main.pk +'" class="news_item_page">'+
        '<div class="news_page_content">';
          item_page_html +=
          '<div class="news_page_title">'+ main.title +'</div>'+
          '<div class="news_page_desc">'+
            '<!--span style="color:#394246;">'+
              '<p></p>'+
            '</span-->'+
          '</div>'+
        '</div>'+
        '<div style="clear:both"></div>'+
        '<div class="news_page_detail_tag">'+
          '<div class="news_page_source">'+main.source+'</div>'+
          '<div class="news_page_published_date">'+ main.article_date +'</div>'+
          '<div style="clear:both"></div>'+
        '</div>'+
        '<div style="clear:both;"></div>'+
        '<div class="news_page_img">';
        if(!(main.image == "noimage"))
          item_page_html += '<img class="item_image" src="newsmedia/'+main.image+'" style="width:100%;"/>';
        item_page_html += '</div>'+
        '<!--div style="clear:both"></div-->'+
        '<div class="news_page_article_content">'+
          main.content +
        '</div>'+
      '</div>';
      if(related.length > 0) {
        item_page_html += ''+
        '<div id="related_items_'+ main.pk +'" class="related_items_box">'+
          '<div style="clear:both"></div>'+
          '<div class="related_items_header">Related News</div>';
          for(var j=0; j<related.length; j++) {
            item_page_html += ''+
            '<div class="related_items">'+
              construct_related_item(related[j]) +
            '</div>';
          }
          item_page_html += '</div>';
      }
     $("#content").html(item_page_html);


     /* Internal content links, image sizes handled */
     /*
     $('.news_page_article_content a').attr('target', '_blank');
     var image_width = $('.news_page_img').width();
     if(image_width > 300) {
        $('.news_page_img').css('width', '100%');

     }
     */
}

function get_by_cat( arg ) {
  console.log("IN GET_BY_CAT");
  console.log(current_selected_source);
  switch( arg )
  {
    case "national":
      $("#content").load('/news/national/', function(res){
        if(res.msg == "NOUSER") { location.hash = 'news/'; }
        res = jQuery.parseJSON(res);
        var content = construct_content(res, 'National');
        $("#content").html(content);
      });
      break;
    case "international":
      $("#content").load('/news/international/', function(res){
        if(res.msg == "NOUSER") { location.hash = 'news/'; }
        res = jQuery.parseJSON(res);
        var content = construct_content(res, 'International');
        $("#content").html(content);
      });
      break;
    case "sports":
      $("#content").load('/news/sports/', function(res){
        if(res.msg == "NOUSER") { location.hash = 'news/'; }
        res = jQuery.parseJSON(res);
        var content = construct_content(res, 'Sports');
        $("#content").html(content);
      });
      break;
    case "entertainment":
      $("#content").load('/news/entertainment/', function(res){
        if(res.msg == "NOUSER") { location.hash = 'news/'; }
        res = jQuery.parseJSON(res);
        var content = construct_content(res, 'Entertainment');
        $("#content").html(content);
      });
      break;
    case "technology":
      $("#content").load('/news/technology/', function(res){
        if(res.msg == "NOUSER") { location.hash = 'news/'; }
        res = jQuery.parseJSON(res);
        var content = construct_content(res, 'Technology');
        $("#content").html(content);
      });
      break;
    case "education":
      $("#content").load('/news/education/', function(res){
        if(res.msg == "NOUSER") { location.hash = 'news/'; }
        res = jQuery.parseJSON(res);
        var content = construct_content(res, 'Education');
        $("#content").html(content);
      });
      break;
    case "health":
      $("#content").load('/news/health/', function(res){
        if(res.msg == "NOUSER") { location.hash = 'news/'; }
        res = jQuery.parseJSON(res);
        var content = construct_content(res, 'Health');
        $("#content").html(content);
      });
      break;
    default: break;
  }
}

function get_by_source(source) {
  location.href = "#news/"+ source.toLowerCase() +'/';
  current_selected_source = source;
  var data = {'source': source};
  var html_content =
  '<div id="news-header">'+
    '<div id="news_heading">'+ source +'</div>'+
    '<div id="news_home">'+
      '<div class="button2" onclick="location.hash=\'news\'">'+
        'Home'+
      '</div>'+
    '</div>'+
    '<div style="clear:both;"></div>'+
  '</div>'+
  '<div style="clear:both;"></div>'+
  '<div id="news_items_block">';
  $.post('/news/source/', data, function(res){
    if(res.msg == "NOUSER") { location.hash = 'news/'; }
    var items_array = res.news;
    var marker = res.marker;
    for(var i=0; i<items_array.length; i++)
    {
      html_content += construct_item(items_array[i]);
    }
    html_content +=
    '</div>'+
    '<input type="hidden" name="marker_'+ source +'" value="'+ marker +'"/>'+
    '<button onclick=\'fetch_more_news("'+ source +'");\'>See More...</button>';
    $('#content').html( html_content );
  });
}

function construct_item(data) {
  var item_html = '';
  item_html =
    '<div id="item_'+ data.pk +'" class="item">'+
      '<div class="item_top_content">'+
        '<div class="item_img">';
          if(!(data.image == "noimage"))
            item_html += '<img src="newsmedia/'+data.image+'">';
        item_html +=
        '</div>'+
        '<div class="news_content">';

        item_html +=
        '<div class="item_title" onclick=location.href="#news/item/'+ data.pk +'/" >'+
          '<span>'+ data.title +'</span>'+
        '</div>'+
        '<div class="item_desc">'+
          '<span style="color:#394246;">'+
            '<p>'+data.description_text+'</p>'+
          '</span>'+
        '</div>'+
        '<div class="read_more_btn">'+
          '<a href="#news/item/'+ data.pk +'">Continue reading...</a>'+
        '</div>'+
        '<div style="clear:both"></div>'+
        '</div>'+
        '<div style="clear:both"></div>'+
      '</div>'+
      '<div class="detail_tag_box">'+
        '<div class="detail_tag">'+
          '<div class="source" onclick=\'get_by_source("'+ data.source +'");\'>'+ data.source +', </div>'+
          '<div class="published_date">'+ data.article_date +'</div>'+
        '</div>'+
        '<div style="clear:both;"></div>'+
      '</div>'+
      '<div style="clear:both;"></div>'+
    '</div>';
  return item_html;
}

function construct_content(res, channel) {
  var items_array = res.news;
  var marker = res.marker;
  var html =
  '<div id="news-header">'+
    '<div id="news_heading">'+ channel +'</div>'+
    '<div id="news_home">'+
      '<div class="button2" onclick="location.hash=\'news\'">'+
        'Home'+
      '</div>'+
    '</div>'+
    '<div style="clear:both;"></div>'+
  '</div>'+
  '<div style="clear:both;"></div>'+
  '<div id="news_items_block">';
    for(var i=0; i<items_array.length; i++)
    {
      html = html + construct_item(items_array[i]);
    }
  html +=
  '</div>'+
  ''+
  '<input type="hidden" name="marker_'+ channel +'" value="'+ marker +'"/>'+
  '<button onclick=fetch_more_news("'+ channel +'");>See More...</button>';
  return html
}

/* CUSTOMIZE PAGE */
var customize_page = function() {
  var html =
      '<div id="news-header">'+
        '<div id="news_heading">Preferences / channels </div>'+
        '<div id="news_home">'+
          '<div class="button2" onclick="location.hash=\'news\'">'+
            'Home'+
          '</div>'+
        '</div>'+
        '<div style="clear:both;"></div>'+
      '</div>'+
      '<div style="clear:both;"></div>'+
      '<div id="custom_box">';
        for(var i=0; i<channel_arr.length; i++) {
          html += '<div class="channel_pref_bars"><div class="channel_name_boxes">'+ channel_arr[i] +'</div><div class="pref_bars" id="pref_'+ channel_arr[i] +'"></div></div>';
        }
        html += '<div style="clear:both;"></div>'+
      '</div>';
  $('#content').html(html);

  $.post('/news/customize/', function(res){
    console.log(res);
    for(var i=0; i<channel_arr.length; i++) {
      var _channel = (res.c_prefs)[i].channel;
      var _value = (res.c_prefs)[i].value;
      $('#pref_'+channel_arr[i]).slider("value", _value);
    }
  });

  $('.pref_bars').slider({
    stop: function( event, ui ) {
      var that = $(this).attr('id');
      var data = {'element_id': that, 'value': ui.value};
      $.post('/news/update/c_prefs/', data, function(res){
         alert("Preferences updated");
         console.log(res)
      });
    }
  });

/*
$(function () {
    $('#custom_box').highcharts({
        chart: {
            animation: false,
            zoomType: 'Y',
            type: 'bar',
            spacingBottom: 15,
            spacingTop: 10,
            spacingLeft: 10,
            spacingRight: 30,
        },
        title: {
            text: 'News Preferences'
        },
        xAxis: {
            categories: ['The Hindu', 'Indian Express', 'Times Of India', 'BBC News', 'MSN News', 'Yahoo News'],
        },
        plotOptions: {
          series: {
            cursor: 'col-resize',
            point: {
              events: {
                drag: function(e) { console.log("dragging!"); },
                drop: function(e) { console.log("dragged!"); }
              }
           },
           stickyTracking: false
          }
        },
        yAxis: {
            data: [50, 90, 99, 30, 60, 75],
            title: {
                text: 'Preference in a scale of 100'
            }
            //max: 100,
            //min: 0
        },
        tooltip: {
          enabled: false
        },
        series: [{
            name: 'Preference',
            //data: [50, 90, 99, 30, 60, 75],
            draggable: true,
            dragMin: 0,
            dragMax: 100,
            //minPointLength: 10
        }],
   });
});*/

}
/* CUSTOMIZE PAGE ENDS */


function fetch_more_news(arg) {  // arg can be 'channel' or 'source'
  var data = {'marker': $('input[name="marker_'+ arg +'"]').val(), 'arg': arg};
  //var marker = $('input[name="marker_'+ arg +'"]').val();
  //var url = '/news/fetch/'+ arg +'/'+ marker +'/';
  var html_content = '';
  $.post('/news/fetch/', data, function(res){
    if(res.msg == "NOUSER") { location.hash = 'news/'; }
    console.log(res);
    var items_array = res.news;
    var new_marker = res.marker;
    for(var i=0; i<items_array.length; i++)
    {
      html_content += construct_item( items_array[i] );
    }
    $('#news_items_block').append( html_content );
    $('input[name="marker_'+ arg +'"]').val( new_marker );
  });
}


