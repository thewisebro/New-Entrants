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

var current_selected_source = "";

$(document).on('load_app_news', function(){
  if(!user.is_authenticated){
    redirect_to_home();
    return;
}

  var args = arguments;

    $.get('/news/categories_list/', {}, function(res){
     var cat_arr = res.categories;
     console.log(cat_arr);
     var content = '<div id="news_cat">'+
        '<div id="labels news-labels">'+
          '<div id="labels-body">'+
            '<div class="label active-label" onclick=label_clicked("All");>'+
              '<div class="label-name">All</div>'+
            '</div>';
     for(var i=0; i<cat_arr.length; i++)
     {
        content += '<div class="label" onclick=label_clicked("'+ cat_arr[i] +'");>'+
                      '<div class="label-name">'+ cat_arr[i] +'</div>'+
                   '</div>';
     }
     content += "</div></div></div>";
     $('.content').html(content);
    });


  console.log(args);
  console.log(args.length);
  switch (args.length)
  {
    case 1:
      if(!(args[0] === null)) {
        $.get('/news/', function(res){
          get_home( res );
        });
      }
      break;
    case 2:
      if((!(args[0] === null) && args[1] === "")) {
        $.get('/news/', function(res){
         get_home( res );
        });
      }
      get_by_cat( args[1] );
      break;
    case 3:
      if(!(args[0] === null) && !(args[1] === null) && args[2] === "") {
        get_by_cat( args[1] );
      }
      if(!(args[0] === null) && args[1] === "item" && !(args[2] === "")) {
        console.log("3-2");
        $.get('/news/item/'+args[2], function(res){
          get_item_page( res );
        });
      }
      break;
    case 4:
      if(!(args[0] === null) && !(args[1] === null) && !(args[2] === null) && args[3] === "") {
        console.log("4-1");
        $.get('/news/item/'+args[2], function(res){
          get_item_page( res );
        });
      }
    default: break;
  }

});

$(document).on("logout", function(){
  redirect_to_home();
});

function get_home( res ) {
  current_selected_source = '';
  $("#content").load('/news/', function(res){
    res = jQuery.parseJSON(res);
    var content = construct_content(res, 'News');
    $("#content").html(content);
  });
}

function get_item_page( res ) {
    var data = res.item;
    current_selected_source = '';
    console.log(data);

    var item_page_html =
      '<div id="news-header">'+
        '<div id="news_heading">'+ data.channel +'</div>'+
        '<div id="news_home">'+
          '<div class="button2" onclick="location.hash=\'news\'">'+
            'Home'+
          '</div>'+
        '</div>'+
        '<div style="clear:both;"></div>'+
      '</div>'+
      '<div style="clear:both;"></div>'+
      '<div id="news_item_'+ data.pk +'" class="news_item_page">'+
        '<div class="news_page_content">';
          item_page_html +=
          '<div class="news_page_title">'+ data.title +'</div>'+
          '<div class="news_page_desc">'+
            '<!--span style="color:#394246;">'+
              '<p></p>'+
            '</span-->'+
          '</div>'+
        '</div>'+
        '<div style="clear:both"></div>'+
        '<div class="news_page_detail_tag">'+
          '<div class="news_page_source">'+data.source+'</div>'+
          '<div class="news_page_published_date">'+ data.article_date +'</div>'+
          '<div style="clear:both"></div>'+
        '</div>'+
        '<div style="clear:both;"></div>'+
        '<div class="news_page_img">';
        if(!(data.image == "noimage"))
          item_page_html += '<img class="item_image" src="media/news/'+data.image+'" style="width:100%;"/>';
        item_page_html += '</div>'+
        '<div style="clear:both"></div>'+
        '<div class="news_page_article_content">'+
          data.content
        '</div>'+
      '</div>';
     $("#content").html(item_page_html);
     $('.news_page_article_content a').attr('target', '_blank');
}

function get_by_cat( arg ) {
  switch( arg )
  {
    case "national":
      $("#content").load('/news/national/', function(res){
        res = jQuery.parseJSON(res);
        var content = construct_content(res, 'National');
        $("#content").html(content);
      });
      break;
    case "international":
      $("#content").load('/news/international/', function(res){
        res = jQuery.parseJSON(res);
        var content = construct_content(res, 'International');
        $("#content").html(content);
      });
      break;
    case "sports":
      $("#content").load('/news/sports/', function(res){
        res = jQuery.parseJSON(res);
        var content = construct_content(res, 'Sports');
        $("#content").html(content);
      });
      break;
    case "entertainment":
      $("#content").load('/news/entertainment/', function(res){
        res = jQuery.parseJSON(res);
        var content = construct_content(res, 'Entertainment');
        $("#content").html(content);
      });
      break;
    case "technology":
      $("#content").load('/news/technology/', function(res){
        res = jQuery.parseJSON(res);
        var content = construct_content(res, 'Technology');
        $("#content").html(content);
      });
      break;
    case "education":
      $("#content").load('/news/education/', function(res){
        res = jQuery.parseJSON(res);
        var content = construct_content(res, 'Education');
        $("#content").html(content);
      });
      break;
    case "health":
      $("#content").load('/news/health/', function(res){
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
    console.log(res);
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
            item_html += '<img src="media/news/'+data.image+'">';
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
  '<input type="hidden" name="marker_'+ channel +'" value="'+ marker +'"/>'+
  '<button onclick=fetch_more_news("'+ channel +'");>See More...</button>';
  return html
}

function fetch_more_news(arg) {  // arg can be 'channel' or 'source'
  var data = {'marker': $('input[name="marker_'+ arg +'"]').val(), 'arg': arg};
  var html_content = '';
  $.post('/news/fetch/', data, function(res){
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

