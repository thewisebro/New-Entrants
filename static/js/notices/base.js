var no_of_pages, last_page_notices;		//variables for search results
var pages, last_page_no;		//variables for show_uploads results
var store = new Array(50);
var emptyarray = new Array(50);
var privelege=0, first_time_visit=0, starred=0;
var search_store, check_upload_array={}, upload_array, star_array={}, read_array={};				      //star_array stores the ids of notices who are starred for a particualar user.read_array is similar
							                                  //search_store stores the results of a particular search
$(document).on("load_app_notices", function(e, hash1, hash2){
  if(hash1 == undefined || hash1 == "")
  {
    location.hash = '#notices/1';
  }
  else if(hash1 == "content")
  {
      display_notice(parseInt(hash2));
  }
  else
  {
    	$('#content').html('Welcome To Notice Board!<br>');
    	if(!(0 in store) || !(49 in store))
    	{
      		gap_scanner(1, 1);
    	}
		get_privelege(hash1, hash2);
  }
});

function get_privelege(hash1, hash2)
{
	if(first_time_visit==0)
	{
		$.ajax({
    		type: 'get',
    		url : 'notices/privelege/',
    		success: function (data)
    		{
			      starred=1;
      			if(data.privelege)
      			{
				      privelege=1;
        			$('a#Upload').remove();
        			html = '<a id = "Upload" href="notices/upload/">Upload</a><br>';
        			html += '<div id = "show_uploads" onclick="upload_change_page(1)">Show/Edit Uploads</div><br>';
        			$('#content').append(html);
      			}
			      search_bar(hash1, hash2);
    		},
		    error: function ()
		    {
			    search_bar(hash1, hash2);
		    }
  });
	}
	else
	{
		if(privelege==1)
		{
        		$('a#Upload').remove();
        		html = '<a id = "Upload" href="notices/upload/">Upload</a><br>';
        		html += '<div id = "show_uploads" onclick="upload_change_page(1)">Show/Edit Uploads</div><br>';
        		$('#content').append(html);
		}
		search_bar(hash1, hash2);
	}
}

function search_bar(hash1, hash2)
{
	html = 'Search: <input type="text" id="search_data" onkeydown="if (event.keyCode == 13) search()"><br>'
	$('#content').append(html);
	if(first_time_visit==0)
	{
		if(starred==1)
    {
      bring_starred_notices(hash1, hash2);
    }
		else
		get_total_notices_no(hash1);
		first_time_visit=1;
	}
	else
  {
    if(hash1 == "search")
    {
      display_search_list(parseInt(hash2));
    }
    else if(hash1 == "show_uploads")
    {
      if(hash2==undefined||hash2=="")
	    show_uploads(1);
      else
	    show_uploads(parseInt(hash2));
    }
    else
    {
	    load_numbers_bar(hash1);
    }
  }
}

function get_total_notices_no(hash1, hash2)
{
  		$.ajax({
    		type: 'get',
    		url : 'notices/max_notices/',
    		success: function (data)
    		{
      			notices_on_last_page = data.total_notices%10;
      			total_pages = Math.floor(data.total_notices/10) ;
      			if (notices_on_last_page > 0)
        		total_pages++;
            if(hash1=="search")
            {
              search();
            }
            else if(hash1=="show_uploads")
            {
              if(hash2!=undefined&&hash2!="")
              show_uploads(parseInt(hash2));
              else
              {
                upload_change_page(1);
              }
            }
            else
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
        html += '<span id="number-' + (i+1) + '" class="numbers_list" onclick="change_page('+ (i+1) + ')">' + (i+1) +'</span>';
      }
      html += '<span id="number-' + total_pages + '"class="numbers_list" onclick="change_page('+ total_pages +  ')">' + total_pages + '</span>';
      html += '</div>';
      $('#content').append(html);
      first_time_check(parseInt(hash1));
}

function change_page(number)
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
function open_notice(id)
{
  location.hash = '#notices/content/' + id;
}

function upload_change_page(page_no)
{
  location.hash = '#notices/show_uploads/' + page_no;
}

function search_change_page(page_no)
{
  url_temp = '#notices/search/' + page_no;
  if(location.hash == url_temp)
  {
  	hashtags = ["search", String(page_no)];
  	$(document).trigger("load_app_notices", hashtags);
  }
  else
  {
	location.hash=url_temp;
  }
}

function list_notices(page_no)
{
  console.log();
      $('div#notice_list').remove();
      html = '<div id="notice_list">';
      var k = 0;
      if(page_no < total_pages || (page_no == total_pages && notices_on_last_page==0))
        k = 10;
      else
        k = notices_on_last_page;
      var a=(page_no-1)*10, b=a+k;
      if(starred==1)
      {
        for(var i=a; i<b; i++)
        {
            if(check_upload_array[store[i].id]==1)
            {
              if(read_array[store[i].id]==1)
              {
                if(star_array[store[i].id]==1)
                {
                  html += '<div style="background-color:gray;" class="notice_info" id="notice_' + store[i].id + '" onclick="open_notice(' + store[i].id + ')">' + '<span class="read" id=notice_read_' + store[i].id + '>R&nbsp</span><span class="starred" onclick="star_notice(' + store[i].id + ', event)">S&nbsp</span>' + store[i].subject + '<span class="edit"><a href="notices/edit_notice/' + store[i].id + '">&nbsp&nbspEdit</a></span></div>';
                }
                else
                {
                  html += '<div class="notice_info" id="notice_' + store[i].id + '" onclick="open_notice(' + store[i].id + ')">' + '<span class="read" id=notice_read_' + store[i].id + '></span>R&nbsp<span class="starred" onclick="star_notice(' + store[i].id + ', event)">S&nbsp</span>' + store[i].subject + '<span class="edit"><a href="notices/edit_notice/' + store[i].id + '">&nbsp&nbspEdit</a></span></div>';
                }
              }

              else
              {
                if(star_array[store[i].id]==1)
                {
                  html += '<div style="background-color:gray;" class="notice_info" id="notice_' + store[i].id + '" onclick="open_notice(' + store[i].id + ')">' + '<span class="read" id=notice_read_' + store[i].id + '></span><span class="starred" onclick="star_notice(' + store[i].id + ', event)">S&nbsp</span>' + store[i].subject + '<span class="edit"><a href="notices/edit_notice/' + store[i].id + '">&nbsp&nbspEdit</a></span></div>';
                }
                else
                {
                  html += '<div class="notice_info" id="notice_' + store[i].id + '" onclick="open_notice(' + store[i].id + ')">' + '<span class="read" id=notice_read_' + store[i].id + '></span><span class="starred" onclick="star_notice(' + store[i].id + ', event)">S&nbsp</span>' + store[i].subject + '<span class="edit"><a href="notices/edit_notice/' + store[i].id + '">&nbsp&nbspEdit</a></span></div>';
                }
              }
            }
           else
           {
              if(read_array[store[i].id]==1)
              {
                if(star_array[store[i].id]==1)
                {
                  html += '<div style="background-color:gray;" class="notice_info" id="notice_' + store[i].id + '" onclick="open_notice(' + store[i].id + ')">' + '<span class="read" id=notice_read_' + store[i].id + '>R&nbsp</span><span class="starred" onclick="star_notice(' + store[i].id + ', event)">S&nbsp</span>' + store[i].subject + '</div>';
                }
                else
                {
                  html += '<div class="notice_info" id="notice_' + store[i].id + '" onclick="open_notice(' + store[i].id + ')">' + '<span class="read" id=notice_read_' + store[i].id + '></span>R&nbsp<span class="starred" onclick="star_notice(' + store[i].id + ', event)">S&nbsp</span>' + store[i].subject + '</div>';
                }
              }

              else
              {
                if(star_array[store[i].id]==1)
                {
                  html += '<div style="background-color:gray;" class="notice_info" id="notice_' + store[i].id + '" onclick="open_notice(' + store[i].id + ')">' + '<span class="read" id=notice_read_' + store[i].id + '></span><span class="starred" onclick="star_notice(' + store[i].id + ', event)">S&nbsp</span>' + store[i].subject + '</div>';
                }
                else
                {
                  html += '<div class="notice_info" id="notice_' + store[i].id + '" onclick="open_notice(' + store[i].id + ')">' + '<span class="read" id=notice_read_' + store[i].id + '></span><span class="starred" onclick="star_notice(' + store[i].id + ', event)">S&nbsp</span>' + store[i].subject + '</div>';
                }
              }
           }
        }
      }
      else
      {
        for(var i=a; i<b; i++)
        {
          html += '<div class="notice_info" onclick="open_notice(' + store[i].id + ')">' + store[i].subject + '</div>';
        }
      }
      html += '</div>';
      $('#content').append(html);
}

function display_notice(id)
{
  $.ajax({
    type: 'get',
    url : 'notices/get_notice/' + id,
    success: function (data)
  console.log("gaind");
  read_notice(id);
  $.ajax({
    type: 'get',
    url : 'notices/get_notice/' + id,
    success: function(data)
    {
      console.log(data.subject);
      html = '<p>Subject : ' + data.subject + '<br>';
      html += 'Reference : ' + data.reference + '<br>';
      html += 'Category : ' + data.uploader.category.name + '<br>';
      html += 'Category : ' + data.category + '<br>';
      html += 'Content : ' + data.content + '<br></p>';
      $('#content').empty();
      $('#content').append(html);
    },
    error: function(data)
    {
      html = ("Error");
      $('#content').empty();
      $('#content').append(html);
    }
  });
}

function gap_filler(llim, hlim, temp, page_no)
{
      $.ajax({
      type: 'get',
      url : 'notices/list_notices/' + llim + '/' + hlim + '/' + temp,
      success: function (data)
      {
           for(var i = llim; i<=hlim; i++)
           {
                store[i] = data[i-llim];
           }
           if(page_no)
           list_notices(page_no);
      }
    });
}

function first_time_check(page_no)                                         /* Check if one clicks for the first time on a bundle*/
{
    var bundle_no = (page_no-1)/5 + 1;
    var len = (store.length/50);
    for(var i=0; i<(bundle_no-len); i++)
      store.push.apply(store, emptyarray);
    gap_scanner(page_no, 0);
}

function gap_scanner(page_no, t)                 // Fills the appropriate gaps with notice objects into the store, between indices
{                                                                           // corresponding to the bundle_no.
	var bundle_no = (page_no-1)/5 + 1;
    var b = bundle_no*50 -1;
    var i = b - 49;
    var gap_begin = 0, gap_end = 0, temp=0;
    while(i!=b+1)
    {
      if(!(i in store) && temp==0)
      {
        gap_begin = i;
        gap_end = 0;
        temp=1;
      }
      if(temp)
      {
        if(i in store)
        gap_end = i - 1;
        else if(i == b)
        gap_end = i;
        else
        {
          i++;
          continue;
        }
        if(t==1)
        {
          gap_filler(gap_begin, gap_end, 0, 0);
        }
        else
        gap_filler(gap_begin, gap_end, store[0].id, page_no);
        gap_begin = 0;
        temp=0;
      }
      i++;
    }
    if(!gap_end)
    list_notices(page_no);
}

function search()
{
	j=0;
	query1=$("#search_data").val();
	if(query1=="")
	j=1;
	query=query1.split(" ");
	t=0;
	k=query.length;
	if(j!=1)
	{
		for(var i=0; i<k;i++)
		{
			if(query[t]=="")
			query.splice(t,1);
			else
	 		t++;
		}
	}
	url="";
	for(var i=0; i<query.length-1; i++)
	{
		url+=query[i]+"+";
	}
	url+=query[query.length-1];
  $.ajax({
      type: 'get',
      url : 'notices/search/?q=' + url,
      success: function (data)
      {
		    len=Object.keys(data).length;
		    no_of_pages=Math.floor(len/10);
        last_page_notices=len%10;
        if(last_page_notices>0)
        no_of_pages++;
        search_store = new Array(len);
        search_store = data;
        search_change_page(1);
      }
    });
}

function display_search_list(page_no)
{
      		$('#page_numbers').remove();
		html = '<div id="page_numbers">';
      		for(var i=0; i<no_of_pages-1; i++)
      		{
        		html += '<span id="number-' + (i+1) + '" class="numbers_list" onclick="search_change_page('+ (i+1) + ')">' + (i+1) +'</span>';
      		}
      		html += '<span id="number-' + no_of_pages + '"class="numbers_list" onclick="search_change_page('+ no_of_pages +  ')">' + no_of_pages + '</span>';
      		html += '</div>';
      		$('#content').append(html);
      $('div#notice_list').remove();
      html = '<div id="notice_list">';
	var k = 0;
      if(page_no < no_of_pages || (page_no == no_of_pages && last_page_notices==0))
        k = 10;
      else
        k = last_page_notices;
      var a=(page_no-1)*10, b=a+k;
	if(starred==1)
	{
      for(var i=a; i<b; i++)
      {
              if(check_upload_array[search_store[i].id]==1)
              {
                if(read_array[search_store[i].id]==1)
                {
                  if(star_array[search_store[i].id]==1)
                  {
                    html += '<div style="background-color:gray;" class="notice_info" id="notice_' + search_store[i].id + '" onclick="open_notice(' + search_store[i].id + ')">' + '<span class="read" id=notice_read_' + search_store[i].id + '>R&nbsp</span><span class="starred" onclick="star_notice(' + search_store[i].id + ', event)">S&nbsp</span>' + search_store[i].subject + '<span class="edit"><a href="notices/edit_notice/' + search_store[i].id + '">&nbsp&nbspEdit</a></span></div>';
                  }
                  else
                  {
                    html += '<div class="notice_info" id="notice_' + search_store[i].id + '" onclick="open_notice(' + search_store[i].id + ')">' + '<span class="read" id=notice_read_' + search_store[i].id + '></span>R&nbsp<span class="starred" onclick="star_notice(' + search_store[i].id + ', event)">S&nbsp</span>' + search_store[i].subject + '<span class="edit"><a href="notices/edit_notice/' + search_store[i].id + '">&nbsp&nbspEdit</a></span></div>';
                  }
                }

                else
                {
                  if(star_array[search_store[i].id]==1)
                  {
                    html += '<div style="background-color:gray;" class="notice_info" id="notice_' + search_store[i].id + '" onclick="open_notice(' + search_store[i].id + ')">' + '<span class="read" id=notice_read_' + search_store[i].id + '></span><span class="starred" onclick="star_notice(' + search_store[i].id + ', event)">S&nbsp</span>' + search_store[i].subject + '<span class="edit"><a href="notices/edit_notice/' + search_store[i].id + '">&nbsp&nbspEdit</a></span></div>';
                  }
                  else
                  {
                    html += '<div class="notice_info" id="notice_' + search_store[i].id + '" onclick="open_notice(' + search_store[i].id + ')">' + '<span class="read" id=notice_read_' + search_store[i].id + '></span><span class="starred" onclick="star_notice(' + search_store[i].id + ', event)">S&nbsp</span>' + search_store[i].subject + '<span class="edit"><a href="notices/edit_notice/' + search_store[i].id + '">&nbsp&nbspEdit</a></span></div>';
                  }
                }
              }
              else
              {
                  if(read_array[search_store[i].id]==1)
                  {
                    if(star_array[search_store[i].id]==1)
                    {
                      html += '<div style="background-color:gray;" class="notice_info" id="notice_' + search_store[i].id + '" onclick="open_notice(' + search_store[i].id + ')">' + '<span class="read" id=notice_read_' + search_store[i].id + '>R&nbsp</span><span class="starred" onclick="star_notice(' + search_store[i].id + ', event)">S&nbsp</span>' + search_store[i].subject + '</div>';
                    }
                    else
                    {
                      html += '<div class="notice_info" id="notice_' + search_store[i].id + '" onclick="open_notice(' + search_store[i].id + ')">' + '<span class="read" id=notice_read_' + search_store[i].id + '></span>R&nbsp<span class="starred" onclick="star_notice(' + search_store[i].id + ', event)">S&nbsp</span>' + search_store[i].subject + '</div>';
                    }
                  }

                  else
                  {
                    if(star_array[search_store[i].id]==1)
                    {
                      html += '<div style="background-color:gray;" class="notice_info" id="notice_' + search_store[i].id + '" onclick="open_notice(' + search_store[i].id + ')">' + '<span class="read" id=notice_read_' + search_store[i].id + '></span><span class="starred" onclick="star_notice(' + search_store[i].id + ', event)">S&nbsp</span>' + search_store[i].subject + '</div>';
                    }
                    else
                    {
                      html += '<div class="notice_info" id="notice_' + search_store[i].id + '" onclick="open_notice(' + search_store[i].id + ')">' + '<span class="read" id=notice_read_' + search_store[i].id + '></span><span class="starred" onclick="star_notice(' + search_store[i].id + ', event)">S&nbsp</span>' + search_store[i].subject + '</div>';
                    }
                }
              }

		}
	}
	else
	{
      		for(var i=a; i<b; i++)
      		{
        		html += '<div class="notice_info" onclick="open_notice(' + search_store[i].id + ')">' + search_store[i].subject + '</div>';
		}
	}
      html += '</div>';
      $('#content').append(html);
}


function star_notice(id, e)
{
	if(e.stopPropagation)
    	e.stopPropagation();
  	else
    	e.cancelBubble = true;
	if(star_array[id]==1)
	{
		url = 'notices/read_star_notice/'+id+'/'+'remove_starred';
		delete star_array[id];
  		$("#notice_"+id).css("background-color" , "white");
	}
	else
	{
		url = 'notices/read_star_notice/'+id+'/'+'add_starred';
		star_array[id]=1;
  		$("#notice_"+id).css("background-color" , "gray");
	}
	$.ajax({
	type: 'post',
	url: url
	});
}

function read_notice(id)
{
	if(!(id in read_array))
	{
		url = 'notices/read_star_notice/'+id+'/'+'add_read';
		read_array[id]=1;
	  $.ajax({
	  type: 'post',
	  url: url
	  });
  }
}

function bring_starred_notices(hash1, hash2)      			// A function that brings all the starred notice corresponding to a particular user
{
	$.ajax({
	type: 'get',
	url: 'notices/star_notice_list/',
	success: function(data)
	{
		len = Object.keys(data).length;
		for(var i=0;i<len;i++)
		{
			star_array[data[i]]=1;
		}
    bring_read_notices(hash1, hash2)
	}
	});
}

function bring_read_notices(hash1, hash2)      			// A function that brings all the read notice corresponding to a particular user
{
	$.ajax({
	type: 'get',
	url: 'notices/read_notice_list/',
	success: function(data)
	{
		len = Object.keys(data).length;
		for(var i=0;i<len;i++)
    {
			read_array[data[i]]=1;
		}
    if(privelege==1)
    bring_uploads(hash1, hash2)
    else
		get_total_notices_no(hash1);
	}
	});
}

function bring_uploads(hash1, hash2)
{
   $.ajax({
      type: 'get',
      url: 'notices/show_uploads/',
      success: function(data)
      {
        len = Object.keys(data).length;
		    pages=Math.floor(len/10);
        last_page_no=len%10;
        if(last_page_no>0)
        pages++;
        upload_array = new Array(len);
        for(var i=0;i<len;i++)
        {
          upload_array[i] = data[i];
          check_upload_array[data[i].id]=1;
        }
		    get_total_notices_no(hash1, hash2);
      }
   });
}

function show_uploads(page_no)
{
		      html = '<div id="page_numbers">';
      		for(var i=0; i<pages-1; i++)
      		{
        		html += '<span id="number-' + (i+1) + '" class="numbers_list" onclick="upload_change_page('+ (i+1) + ')">' + (i+1) +'</span>';
      		}
      		html += '<span id="number-' + pages + '"class="numbers_list" onclick="upload_change_page('+ pages +  ')">' + pages + '</span>';
      		html += '</div>';
      		$('#content').append(html);
      $('div#notice_list').remove();
      html = '<div id="notice_list">';
	var k = 0;
      if(page_no < pages || (page_no == pages && last_page_no==0))
        k = 10;
      else
        k = last_page_no;
      var a=(page_no-1)*10, b=a+k;
	if(starred==1)
	{
      for(var i=a; i<b; i++)
      {
          if(read_array[upload_array[i].id]==1)
          {
			        if(star_array[upload_array[i].id]==1)
			        {
        			    html += '<div style="background-color:gray;" class="notice_info" id="notice_' + upload_array[i].id + '" onclick="open_notice(' + upload_array[i].id + ')">' + '<span class="read" id=notice_read_' + upload_array[i].id + '>R&nbsp</span><span class="starred" onclick="star_notice(' + upload_array[i].id + ', event)">S&nbsp</span>' + upload_array[i].subject + '<span class="edit"><a href="notices/edit_notice/' + upload_array[i].id + '">&nbsp&nbspEdit</a></span></div>';
			        }
			        else
			        {
        			    html += '<div class="notice_info" id="notice_' + upload_array[i].id + '" onclick="open_notice(' + upload_array[i].id + ')">' + '<span class="read" id=notice_read_' + upload_array[i].id + '></span>R&nbsp<span class="starred" onclick="star_notice(' + upload_array[i].id + ', event)">S&nbsp</span>' + upload_array[i].subject + '<span class="edit"><a href="notices/edit_notice/' + upload_array[i].id + '">&nbsp&nbspEdit</a></span></div>';
			        }
          }

          else
          {
			        if(star_array[upload_array[i].id]==1)
			        {
        			  html += '<div style="background-color:gray;" class="notice_info" id="notice_' + upload_array[i].id + '" onclick="open_notice(' + upload_array[i].id + ')">' + '<span class="read" id=notice_read_' + upload_array[i].id + '></span><span class="starred" onclick="star_notice(' + upload_array[i].id + ', event)">S&nbsp</span>' + upload_array[i].subject + '<span class="edit"><a href="notices/edit_notice/' + upload_array[i].id + '">&nbsp&nbspEdit</a></span></div>';
			        }
			        else
			        {
        			    html += '<div class="notice_info" id="notice_' + upload_array[i].id + '" onclick="open_notice(' + upload_array[i].id + ')">' + '<span class="read" id=notice_read_' + upload_array[i].id + '></span><span class="starred" onclick="star_notice(' + upload_array[i].id + ', event)">S&nbsp</span>' + upload_array[i].subject + '<span class="edit"><a href="notices/edit_notice/' + upload_array[i].id + '">&nbsp&nbspEdit</a></span></div>';
			        }
          }

		}
	}
      html += '</div>';
      $('#content').append(html);
}
