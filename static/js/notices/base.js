var no_of_pages, last_page_notices;		//variables for search results
var pages, last_page_no;		//variables for show_uploads results
var total_pages, notices_on_last_page;		//variables for general new notice display(all)
var old_total_pages, old_notices_on_last_page;		//variables for general expired notice display(all)
var temp_total_pages, temp_notices_on_last_page;		//variables for general notice display(specific category)
var store = new Array(50), temp_store = new Array(50), old_store= new Array(50);    //store stands for new store or the store of new notices.
var emptyarray = new Array(50);
var hash1, hash2, hash3, hash4, hash5, mode="new", more, name_to_display, all=1, same=1, m_category="All", sub_category="All", search_string="";
var privelege=0, first_time_visit=0, starred=0, select_category=0;
var checklist, search_store, check_upload_array={}, upload_array, star_array={}, read_array={};				      //star_array stores the ids of notices who are starred for a particular user.read_array is similar
//search_store stores the results of a particular search

$(document).on("load_app_notices", function(e, h1, h2, h3, h4, h5){
  console.log("abc");
  console.log(h1);
  $("#right-column .content").empty();
  if(h1 == undefined || h1 == "")
  {
    console.log("abcderter");
    hash1="new";
    hash2="All";
    hash3="All";
    hash4="1";
  }
  else
  {
    hash1=h1;
    hash2=h2;
    hash3=h3;
    hash4=h4;
    hash5=h5;
  }
  if(hash1=="new"||hash1=="old")
  {
        if(search_string!="")
          search_string="";
        if(hash2==m_category && hash3==sub_category)
        same=1;
        else
        {
      console.log("abcqw");
          temp_store = new Array(50);
          same=0;
          m_category=hash2;
          sub_category=hash3;
        }
  }

  else if(hash1=="search")
  {
        if(hash3==m_category && hash4==sub_category)
        same=1;
        else
        {
          same=0;
          m_category=hash3;
          sub_category=hash4;
        }
  }
      console.log(m_category);
      if(m_category=="All"&&sub_category=="All")
      {
          all=1;
          if(mode=="new")
          {
            temp_store=store;
            temp_total_pages=total_pages;
            temp_notices_on_last_page=notices_on_last_page;
          }
          else
          {
            temp_store=old_store;
            temp_total_pages=old_total_pages;
            temp_notices_on_last_page=old_notices_on_last_page;
          }
      }
      else
        all=0;
      console.log(all);
      checklist={};
      more=0;
      t=0;
      if(hash1 == "content")
      {
          display_notice(parseInt(hash2));
      }
      else
      {
          $('#content').html(welcome_html());
          if(!(0 in temp_store) || !(49 in temp_store))
          {
      console.log("bharat");
              gap_scanner(1, 1);
          }
          else
          {
      console.log("bharat5");
      console.log(same);
            get_privelege();
          }
      }
});

function get_privelege()
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
        			$('#content').append(upload_html());
      			}
			      newold_buttons();
    		},
		    error: function ()
		    {
			    newold_buttons();
		    }
  });
	}
	else
	{
		if(privelege==1)
		{
      console.log("c1")
        		$('a#Upload').remove();
        		$('#content').append(upload_html());
		}
		newold_buttons();
	}
}

function load_cat_bar(name)
{
  $('#content').append(load_cat_bar_html(name));
}

function additional_features()
{
  $('#content').append(additional_features_html());
}

function newold_buttons()
{
  console.log("test1");
	$("#global_search_bar").val("");
	$("#global_search_bar").attr('placeholder', search_string);
	$('#content').append(newold_buttons_html());
  if(starred==1)
	additional_features();
  if(hash1!="show_uploads")
  {
    if(sub_category=="All")
      load_cat_bar(m_category)
    else
      load_cat_bar(sub_category);
  }

  if(first_time_visit==0)
	{
		if(starred==1)
    {
      console.log("gsda");
      bring_starred_notices();
    }
		else
		get_total_notices_no();
    if(all==1)
      first_time_visit=1;
	}
	else
  {
      console.log("testw1");
      console.log("gsdad");
    if(hash1 == "search")
    {
      if(hash5==undefined||hash5==""||same==0)
	    search();
      else
      {
        console.log("before_loading_search_number_bar")
        load_numbers_bar(no_of_pages, "search_");
        console.log("before_loading_search_results")
        list_notices(parseInt(hash5), search_store, no_of_pages, last_page_notices);
        console.log("after_loading_search_results")
      }
    }
    else if(hash1 == "show_uploads")
    {
      load_numbers_bar(pages, "upload_");
      if(hash3==undefined||hash3=="")
	    list_notices(1, upload_array, pages, last_page_no);
      else
	    list_notices(parseInt(hash3), upload_array, pages, last_page_no);
    }
    else if(all==1)
    {
      console.log("bhaerat");
	    load_numbers_bar(temp_total_pages, "");
    }
    else
    {
      if(same==0)
	      get_total_notices_no();
      else
        load_numbers_bar(temp_total_pages, "");
    }
  }
}

function get_total_notices_no()
{
      if(all==1||first_time_visit==0)
      {
  		  $.ajax({
    		  type: 'get',
    		  url : 'notices/max_notices/',
    		  success: function (data)
    		  {
          console.log(data);
      			  notices_on_last_page = data['total_new_notices']%10;
      			  total_pages = Math.floor(data['total_new_notices']/10) ;
      			  if (notices_on_last_page > 0)
        		    total_pages++;

              old_notices_on_last_page = data['total_old_notices']%10;
      			  old_total_pages = Math.floor(data['total_old_notices']/10) ;
              if (old_notices_on_last_page > 0)
        		    old_total_pages++;
              temp_total_pages=total_pages;
              temp_notices_on_last_page=notices_on_last_page;

            if(hash1=="search")
            {
              search();
            }
            else if(hash1=="show_uploads")
            {
              if(hash3!=undefined&&hash3!="")
              {
                load_numbers_bar(pages, "upload_");
                list_notices(parseInt(hash3), upload_array, pages, last_page_no);
              }
              else
              {
                upload_change_page(1);
              }
            }
            else if(all==0)                 //Something done to control if url has a category other than All/All when the page opens for the first time.
            {
              console.log("wierdo");;
              first_time_visit=-1;
              temp_store = new Array(50);
              gap_scanner(1,1);
            }
            else
      			load_numbers_bar(temp_total_pages, "");
    		  }
  		  });
      }
      else
      {
        console.log("231");
  		  $.ajax({
    		  type: 'get',
    		  url : 'notices/temp_max_notices/' + hash1 + '/' + hash2 + '/' + hash3,
    		  success: function (data)
    		  {
      			temp_notices_on_last_page = data.total_notices%10;
      			temp_total_pages = Math.floor(data.total_notices/10) ;
      			if (temp_notices_on_last_page > 0)
        		  temp_total_pages++;
      			load_numbers_bar(temp_total_pages, "");
          }
        });
      }
}

function load_numbers_bar(tp, mode1)
{
      $('div#page_numbers').remove();
      $('#content').append(load_numbers_bar_html(tp, mode1));
      if(mode1=="")
      first_time_check();
}

function change_page(number)
{
  console.log("23");
  location.hash = '#notices/' + hash1 + '/' + hash2 +'/' +  hash3 + '/' +number;
}

function open_notice(id)
{
  location.hash = '#notices/content/' + id;
}

function upload_change_page(page_no)
{
  if(hash1!="show_uploads")
  location.hash = '#notices/show_uploads/new/' + page_no;
  else
  location.hash = '#notices/show_uploads' + hash2 + '/' + page_no;
}

function search_change_page(page_no)
{
  if(hash1 == "show_uploads")
  url_temp = '#notices/search/new/All/All/' + page_no;
  else if(hash1=="new" || hash1=="old")
  url_temp = '#notices/search/' + hash1 + '/' + hash2 + '/' + hash3 + '/' + page_no;
  else
  url_temp = '#notices/search/' + hash2 + '/' + hash3 + '/' + hash4 + '/' + page_no;
  if(location.hash == url_temp)
  {
  	hashtags = ["search", hash2, hash3, hash4, String(page_no)];
  	$(document).trigger("load_app_notices", hashtags);
  }
  else
  {
	location.hash=url_temp;
  }
}

function list_notices(page_no, tstore, ttotal_pages, tnotices_on_last_page)
{
      console.log("listpeaagya");
      $('div#notice_list').remove();
      html = '<div id="notice_list">';
      var k = 0;
      if(page_no < ttotal_pages || (page_no == ttotal_pages && tnotices_on_last_page==0))
        k = 10;
      else
        k = tnotices_on_last_page;
      var a=(page_no-1)*10, b=a+k;
      context = {};
      for(var i=a; i<b; i++)
      {
            context["notice"] = tstore[i]

            if(starred==1)
              context["anonymous"] = 0;
            else
              context["anonymous"] = 1;

            if(check_upload_array[tstore[i].id]==1)
              context["edit"] = 1;
            else
              context["edit"] = 0;

            if(read_array[tstore[i].id]==1)
              context["read"] = 1;
            else
              context["read"] = 0;

            if(star_array[tstore[i].id]==1)
              context["star"] = 1;
            else
              context["star"] = 0;

            $('#content').append(list_notices_html(context));

      }
      html += '</div>';
      $('#content').append(html);
}

function display_notice(id)
{
  read_notice(id);
  $.ajax({
    type: 'get',
    url : 'notices/get_notice/' + id,
    success: function(data)
    {
      $('#content').empty();
      $('#content').append(display_notice_html(data));
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
  console.log("bharat1");
  console.log(temp);
    if(all==1||first_time_visit==0)
    {
  console.log(hlim);
        $.ajax({
        type: 'get',
        url : 'notices/list_notices/' + hash1 + '/' + llim + '/' + hlim + '/' + temp,
        success: function (data)
        {
      console.log("paint");
           for(var i = llim; i<=hlim; i++)
           {
                temp_store[i] = data[i-llim];
           }
           if(!page_no)
           {
              store = temp_store;
           console.log("abcd1");
              get_privelege();
           }
           else
           {
                if(mode=="new")
                  store = temp_store;
                else
                  old_store = temp_store;
                list_notices(page_no, temp_store, temp_total_pages, temp_notices_on_last_page);
            }
        },
      });
    }
    else
    {
  console.log("bharat10");
        $.ajax({
        type: 'get',
        url : 'notices/temp_list_notices/' + hash1 + '/' + hash2 + '/' + hash3 + '/' + llim + '/' + hlim + '/' + temp,
        success: function (data)
        {
           for(var i = llim; i<=hlim; i++)
           {
                temp_store[i] = data[i-llim];
           }
           if(first_time_visit==-1)
           {
            first_time_visit=1;
            get_total_notices_no();
           }
           else if(page_no)
           list_notices(page_no, temp_store, temp_total_pages, temp_notices_on_last_page);
           else
           get_privelege();
        },
      });
    }
}

function first_time_check()                                         /* Check if one clicks for the first time on a bundle*/
{
  page_no=parseInt(hash4);
  var bundle_no = parseInt((page_no-1)/5) + 1;
    if(all==1)
    {
      if(mode=="new")
      {
        var len = (store.length/50);
        for(var i=0; i<(bundle_no-len); i++)
          store.push.apply(store, emptyarray);
        gap_scanner(page_no, 0);
      }
      else
      {
        console.log("old_School");
        console.log(page_no);
        console.log(bundle_no);
        var len = (old_store.length/50);
        for(var i=0; i<(bundle_no-len); i++)
          old_store.push.apply(old_store, emptyarray);
        gap_scanner(page_no, 0);
      }
    }
    else
    {
      var len = (temp_store.length/50);
      for(var i=0; i<(bundle_no-len); i++)
        temp_store.push.apply(temp_store, emptyarray);
      gap_scanner(page_no, -1);
    }
}

function gap_scanner(page_no, t)                 // Fills the appropriate gaps with notice objects into the store, between indices
{                                                                           // corresponding to the bundle_no.
  console.log(temp_store);
  var bundle_no = parseInt((page_no-1)/5) + 1;
    var b = bundle_no*50 -1;
    var i = b - 49;
    var gap_begin = 0, gap_end = 0, temp=0;
    while(i!=b+1)
    {
      if(!(i in temp_store) && temp==0)
      {
        gap_begin = i;
        gap_end = 0;
        temp=1;
      }
      if(temp)
      {
        if(i in temp_store)
          gap_end = i - 1;
        else if(i == b)
          gap_end = i;
        else
        {
          i++;
          continue;
        }
        if(t==1)
          gap_filler(gap_begin, gap_end, 0, 0);
        else
          gap_filler(gap_begin, gap_end, temp_store[0].id, page_no);
        gap_begin = 0;
        temp=0;
      }
      i++;
    }
    if(!gap_end)
    {
      console.log("wqerty");
      list_notices(page_no, temp_store, temp_total_pages, temp_notices_on_last_page);
    }
}

function check_if_date(query2)
{
  console.log("entered check_if_date")
  console.log(query2)
  url=""
  if(query2.split("-").length==2)
  {
    parts=query2.split("-");
    parts[0]=Date.parse(parts[0]);
    parts[1]=Date.parse(parts[1]);
    if(parts[0]>1262284200000 && parts[1]>1262284200000)
    url = ">>" + parts.join().replace(",", "-");
  }
  else if(!isNaN(Date.parse(query2)) && Date.parse(query2)>1262284200000)
  {
    x = Date.parse(query2)
    url = ">>" + x.toString() + "-" + (x+86400000).toString();
  }
    console.log(url);
  return url
}

function search()
{
  console.log("sr");
	j=0;url="";
	query1=$("#global_search_bar").val();
  if(query1=="")
  {
    query1=search_string;
  }
  else
  {
    search_string=query1;
  }
  console.log(search_string);
  check_if_date(search_string)
  if(url=="")
  {
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
  }
          console.log(url);
  $.ajax({
      type: 'get',
      url : 'notices/search/' + mode + '/' + m_category + '/' + sub_category + '/?q=' + url,
      success: function (data)
      {
		    len=Object.keys(data).length;
		    no_of_pages=Math.floor(len/10);
        last_page_notices=len%10;
        if(last_page_notices>0)
        no_of_pages++;
        search_store = new Array(len);
        search_store = data;
        console.log("search_done");
        console.log(search_store);
        console.log("search_ends");
        search_change_page(1);
      }
    });
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
	url: url,
  error : function()
  {
    html = 'Error';
    $('#content').empty();
    $('#content').append(html);
  }
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

function bring_starred_notices()      			// A function that brings all the starred notice corresponding to a particular user
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
    bring_read_notices()
	}
	});
}

function bring_read_notices()      			// A function that brings all the read notice corresponding to a particular user
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
    bring_uploads()
    else
		get_total_notices_no();
	}
	});
}

function bring_uploads()
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
		    get_total_notices_no();
      }
   });
}

function edit_notice(id, e)
{
  window.location.href = 'notices/edit_notice/'+id
	if(e.stopPropagation)
    	e.stopPropagation();
  	else
    	e.cancelBubble = true;
}

function delete_notice(id, e)
{
  var r = confirm("Are you sure you want to delete this Notice? Once Deleted, the Notice cannot be recovered!");
  if(r==true)
  {
    window.location.href = 'notices/delete_notice/'+id;
  }
	  if(e.stopPropagation)
      e.stopPropagation();
  	else
    	e.cancelBubble = true;
}

function add_to_checklist(id, e)
{
  console.log("gaind7");
  var x = document.getElementById("check-" + id).checked;
  if(!x)
    delete checklist[id];
  else
    checklist[id]=1;
	if(e.stopPropagation)
    e.stopPropagation();
  else
    e.cancelBubble = true;
}

function select_all()
{
  var x = document.getElementById("all_select").checked;
  var k;
  if(hash1=="new"||hash1=="old")
  {
    if(parseInt(hash4)<temp_total_pages||temp_notices_on_last_page==0)
      k=10;
    else
      k=temp_notices_on_last_page;
  }
  else
  {
    if(hash1=="show_uploads")
    {
      if(parseInt(hash3)<pages||last_page_no==0)
        k=10;
      else
        k=last_page_no;
    }
    else
    {
      if(parseInt(hash4)<no_of_pages||last_page_notices==0)
        k=10;
      else
        k=last_page_notices;
    }
  }
  if(x)
  {
    $('.check').prop('checked', true);
    for(var i=0; i<k; i++)
    {
        id = $('.check')[i].id[6]+$('.check')[i].id[7];
        checklist[parseInt(id)]=1;
    }
  }
  else
  {
    $('.check').prop('checked', false);
    for(var i=0; i<k; i++)
    {
        id = $('.check')[i].id[6]+$('.check')[i].id[7];
        delete checklist[parseInt(id)];
    }
  }
}

function show_menu(e)
{
	if(e.stopPropagation)
    e.stopPropagation();
  else
    e.cancelBubble = true;
  if(more==1)
  {
    $("#more").css("background-color", "#E7E7E7");
    $("#menu").remove();
    more=0;
  }
  else
  {
    $("#more").css("background-color", "#97968D");
    $('#super_more').append(more_html());
    more=1;
  }
}

function read_star_checklist(t)
{
  console.log("gaind9");
  a = Object.keys(checklist);
  console.log(a);
  k=a.length;
	url = 'notices/mul_read_star_notice/';
  var q = "?q=";
  for(var i=0;i<k;i++)
  {
	  q += a[i]+'+';
    if(t==1)
    {
      m
      m
      m
      m
	    star_array[a[i]]=1;
      $("#notice_"+a[i]).css("background-color" , "gray");
    }
    else if(t==2)
    {
      console.log(a[i]);
		  delete star_array[a[i]];
  	  $("#notice_"+a[i]).css("background-color" , "white");
    }
    else if(t==3)
    {
		  read_array[a[i]]=1;
  	  $("#notice_read_"+a[i]).text("R ");
    }
    else
    {
      delete read_array[a[i]];
  	  $("#notice_read_"+a[i]).empty();
    }
  }
  q=q.substring(0,q.length-1);
  if(t==1)
    url += 'add_starred/';
  if(t==2)
    url += 'delete_starred/';
  if(t==3)
    url += 'add_read/';
  if(t==4)
    url += 'delete_read/';
  $.ajax({
    type: 'post',
    url: url+q,
    error : function()
    {
      $('#content').empty();
      $('#content').append('Error');
    }
	});
}

function display_categories()
{
  console.log("hello");
  if(select_category==0)
  {
    $("#select_category").css("background-color", "#97968D");
    $('#category_master_div').append(display_categories_html());
    select_category=1;
  }
  else
  {
    $("#select_category").css("background-color", "white");
    $('#category_menu').remove();
    select_category=0;
  }
}

function display_sub_categories(main_category)
{
  var len=constants[main_category].length;
  var k=Math.min(len, 11)
  $('#category_child1').empty(); $('#category_child2').empty();
  $('#category_child1').append(display_sub_categories_html(0, k, main_category));
  $('#category_child2').append(display_sub_categories_html(k, len, main_category));
}

function change_category_bar_name(main_category, category)
{
  if(m_category==main_category && sub_category==category)
  {
    m
    $("#select_category").css("background-color", "white");
    $('#category_menu').remove();
    select_category=0;
    return;
  }
  select_category=0;
  if(hash1=="new"||hash1=="old")
  {
    console.log("breakingbad");
    url_temp = '#notices/' + hash1 + '/' + main_category +'/' +  category + '/1';
    location.hash = url_temp;
  }
  else
  {
    url_temp = '#notices/search/' + hash2 + '/' + main_category +'/' +  category + '/1';
    location.hash = url_temp;
  }
}

function newold_clicked(ns)       //ns stands for new status, storing the mode of the button that is clicked.
{
    console.log("newold_clicked");
  if(ns=="old" && !(0 in old_store))
  {
    $.ajax({
        type : 'get',
        url : 'notices/list_notices/old/0/49/0',
        success : function(data)
        {
           for(var i = 0; i<=49; i++)
                old_store[i] = data[i];
            mode="old";
            location.hash = '#notices/old/All/All/1';
        }
        });
  }
  else if(mode!=ns)
  {
    console.log("without");
    if(ns=="old")
    {
      mode="old";
      location.hash = '#notices/old/All/All/1';
    }
    else
    {
      mode="new";
      location.hash = '#notices/new/All/All/1';
    }
  }
}

function welcome_html()
{
      return Handlebars.notices_templates.welcome();
}

function upload_html()
{
    return Handlebars.notices_templates.upload();
}

function load_cat_bar_html(name)
{
    return Handlebars.notices_templates.load_cat_bar({name : name});
}

function additional_features_html()
{
    return Handlebars.notices_templates.additional_features();
}

function newold_buttons_html()
{
    return Handlebars.notices_templates.newold_buttons();
}

function load_numbers_bar_html(tp23, mode1)
{
    numbers = [];
    for(var i=1;i<tp23;i++)numbers.push(i);
    return Handlebars.notices_templates.load_numbers_bar({ tp : tp23 , numbers : numbers, mode1 : mode1});
}

function display_notice_html(data)
{
    return Handlebars.notices_templates.display_notice({data : data});
}

function more_html()
{
    return Handlebars.notices_templates.more();
}

function display_categories_html(a)
{
    var a = Object.keys(constants);
    return Handlebars.notices_templates.display_categories({a : a});
}

function display_sub_categories_html(initi, finali, main_category)
{
    sub_categories = {};
    for(var i=initi;i<finali;i++)
    {
      sub_categories[i] = constants[main_category][i];
    }
    return Handlebars.notices_templates.display_sub_categories({ sub_categories : sub_categories , main_category : main_category});
}

function list_notices_html()
{
    return Handlebars.notices_templates.list_notices(context);
gt}
