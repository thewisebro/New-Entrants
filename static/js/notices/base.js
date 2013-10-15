var total_pages, notices_on_last_page;

$(document).on("load_app_notices", function(e, hash1, hash2){
  if(hash1 == undefined || hash1 == "")
  {
    console.log(hash1);
    location.hash = '#notices/1';
  }
  else
  {
    $('#content').html('Welcome To Notice Board!');
    get_privelege(hash1);
  }
});

function get_privelege(hash1)
{
  $.ajax({
    type: 'get',
    url : 'notices/privelege/',
    success: function (data)
    {
      if(data.privelege)
      {
        $('a#Upload').remove();
        html = '<a id = "Upload" href="notices/upload/">Upload</a>';
        $('#content').append(html);
      }
    get_total_notices_no(hash1);
    }
  });
}

function get_total_notices_no(hash1)
{
  $.ajax({
    type: 'get',
    url : 'notices/max_notices/',
    success: function (data)
    {
      notices_on_last_page = data.total_notices%10;
      total_pages = Math.floor(data.total_notices/10) ;
      if (notices_on_last_page > 0)
      {
        total_pages++;
      }
      load_numbers_bar(hash1);
    }
  });
};

function load_numbers_bar(hash1)
{
      $('div#page_numbers').remove();
      html = '<div id="page_numbers">';
      for(var i=0; i<total_pages-1; i++)
      {
        html += '<span id="number-' + (i+1) + '" class="numbers_list" onclick="hashchange('+ (i+1) + ')">' + (i+1) +'</span>';
      }
      html += '<span id="number-' + total_pages + '"class="numbers_list" onclick="hashchange('+ total_pages +  ')">' + total_pages + '</span>';
      html += '</div>';
      $('#content').append(html);
      list_notices(parseInt(hash1));
}

function hashchange(number)
{
  location.hash = '#notices/' + number;
}

function list_notices(page_no)
{
  $.ajax({
    type: 'get',
    url : 'notices/list_notices/' + page_no,
    success: function (data)
    {
      $('div#notice_list').remove();
      html = '<div id="notice_list">';
      var k = 0;
      if(page_no < total_pages)
        k = 10;
      else
        k = notices_on_last_page;
      for(var i=0; i<k; i++)
      {
        html += '<div class="notice_info" onclick="display_notice(' + data[i].id + ')">'  + data[i].subject + '</div>';
      }
      html += '</div>'
      $('#content').append(html);
    }
  });
}

function display_notice(id)
{
  $.ajax({
    type: 'get',
    url : 'notices/get_notice/' + id,
    success: function (data)
    {
      console.log(data.subject);
      html = '<p>Subject : ' + data.subject + '<br>';
      html += 'Reference : ' + data.reference + '<br>';
      html += 'Category : ' + data.uploader.category.name + '<br>';
      $('#content').empty();
      $('#content').append(html);
    }
  });
}

