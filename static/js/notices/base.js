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

var Authorities = ["All", "Academics", "CPO", "DOSW", "Alumni Affairs", "Construction", "Central Library", "CD", "Deans", "Heads", "Hospital", "Registrar", "Finance", "Ps to Director", "Steno to Deputy Director", "QIP", "Senate", "ISC"];
var Bhawans = ["All", "Azad", "Cautley", "Ganga", "Govind", "Jawahar", "Rajendra", "Ravindra", "Sarojini", "Kasturba", "Malviya", "Rajeev", "Radhakrishnan"];
var Departments = ["All", "Alternative Hydro Energy Centre", "Architecture and Planning", "Biotechnology", "Chemical", "Civil", "Chemistry", "Earth Science", "Earthquake", "Electrical", "Electronics and Computer Science", "Hydrology", "Humanities", "DPT", "Management Studies", "Mechanical and Indstrial", "Metallurgy", "Physics", "Water Resources Development and Management", "Institute Computer Centre"];
var constants = {"All" : [], "Placement" : [], "Authorities" : Authorities, "Bhawans" : Bhawans, "Departments" : Departments}

$(document).on("load_app_notices", function(e, h1, h2, h3, h4, h5){
  console.log("abc");
  console.log(h1);
  $("#right-column").empty();
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
          $('#content').html('Welcome To Notice Board!<br>');
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
        			html = '<a id = "Upload" href="notices/upload/">Upload</a><br>';
        			html += '<div id = "show_uploads" onclick="upload_change_page(1)">Show/Edit Uploads</div><br>';
        			$('#content').append(html);
      			}
			      newold_and_search_bar();
    		},
		    error: function ()
		    {
			    newold_and_search_bar();
		    }
  });
	}
	else
	{
		if(privelege==1)
		{
      console.log("c1")
        		$('a#Upload').remove();
        		html = '<a id = "Upload" href="notices/upload/">Upload</a><br>';
        		html += '<div id = "show_uploads" onclick="upload_change_page(1)">Show/Edit Uploads</div><br>';
        		$('#content').append(html);
		}
		newold_and_search_bar();
	}
}

function load_bar(name)
{
  html = '<div id="category_master_div"><div id="select_category" style="display:inline;width=143px;height:16px;" onclick="display_categories()">' + name + '</div><br></div>';
  $('#content').append(html);
}

function additional_features()
{
  html = '<div id="additional"><div id="main_check" style="float:left;"><input type="checkbox" style="margin-top:2px;" id = "all_select" onclick="select_all()"></div>';
	html += '<div id="super_more"><div id="more" style="background-color:#E7E7E7;float:left;margin-left:146px;" onclick="show_menu(event)">More:</div></div><br><br></div>'
  $('#content').append(html);
}

function newold_and_search_bar()
{
  console.log(all);
	html = '<div id="newold_buttons" style="margin-bottom:4px;"><input type="button" id="new_button" onclick="newold_clicked(\'new\')" value="New">';
	html += '<input type="button" id="old_button" onclick="newold_clicked(\'old\')" value="Old"><br></div>';
	html += '<div id="search_bar">Search: <input type="text" id="search_data" placeholder="' + search_string + '" onkeydown="if (event.keyCode == 13) search()"><br></div>';
	$('#content').append(html);
  if(starred==1)
	additional_features();
  if(hash1!="show_uploads")
  {
    if(sub_category=="All")
      load_bar(m_category)
    else
      load_bar(sub_category);
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
      console.log("gsdad");
    if(hash1 == "search")
    {
      if(hash5==undefined||hash5==""||same==0)
	    search();
      else
      display_search_list(parseInt(hash5));
    }
    else if(hash1 == "show_uploads")
    {
      if(hash3==undefined||hash3=="")
	    show_uploads(1);
      else
	    show_uploads(parseInt(hash3));
    }
    else if(all==1)
    {
      console.log("bhaerat");
	    load_numbers_bar();
    }
    else
    {
      if(same==0)
	      get_total_notices_no();
      else
        load_numbers_bar();
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
              show_uploads(parseInt(hash3));
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
      			load_numbers_bar();
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
      			load_numbers_bar();
          }
        });
      }
}

function load_numbers_bar()
{
      tp=temp_total_pages;
      $('div#page_numbers').remove();
      html = '<div id="page_numbers">';
      for(var i=0; i<tp-1; i++)
      {
        html += '<span id="number-' + (i+1) + '" class="numbers_list" onclick="change_page('+ (i+1) + ')">' + (i+1) +'</span>';
      }
      html += '<span id="number-' + tp + '"class="numbers_list" onclick="change_page('+ tp +  ')">' + tp + '</span>';
      html += '</div>';
      $('#content').append(html);
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

function list_notices(page_no)
{
  console.log("listpeaagya");
      $('div#notice_list').remove();
      html = '<div id="notice_list">';
      var k = 0;
      if(page_no < temp_total_pages || (page_no == temp_total_pages && temp_notices_on_last_page==0))
        k = 10;
      else
        k = temp_notices_on_last_page;
      var a=(page_no-1)*10, b=a+k;
      if(starred==1)
      {
        for(var i=a; i<b; i++)
        {
            if(check_upload_array[temp_store[i].id]==1)
            {
              if(read_array[temp_store[i].id]==1)
              {
                if(star_array[temp_store[i].id]==1)
                {
                  html += '<div style="background-color:gray;" class="notice_info" id="notice_' + temp_store[i].id + '" onclick="open_notice(' + temp_store[i].id + ')">' + '<input type="checkbox" class="check" id="check-' + temp_store[i].id + '" onclick="add_to_checklist(' + temp_store[i].id + ', event)">' + '<span class="read" id=notice_read_' + temp_store[i].id + '>R&nbsp</span><span class="starred" onclick="star_notice(' + temp_store[i].id + ', event)">S&nbsp</span>' + temp_store[i].subject + '<span class="edit" onclick="edit_notice(' + temp_store[i].id + ', event)">&nbsp&nbspEdit</span><span class="delete" onclick="delete_notice(' + temp_store[i].id + ', event)">&nbsp&nbspDelete</span></div>';
                }
                else
                {
                  html += '<div class="notice_info" id="notice_' + temp_store[i].id + '" onclick="open_notice(' + temp_store[i].id + ')">' + '<input type="checkbox" class="check" id="check-' + temp_store[i].id + '" onclick="add_to_checklist(' + temp_store[i].id + ', event)">' + '<span class="read" id=notice_read_' + temp_store[i].id + '>R&nbsp</span><span class="starred" onclick="star_notice(' + temp_store[i].id + ', event)">S&nbsp</span>' + temp_store[i].subject + '<span class="edit" onclick="edit_notice(' + temp_store[i].id + ', event)">&nbsp&nbspEdit</span><span class="delete" onclick="delete_notice(' + temp_store[i].id + ', event)">&nbsp&nbspDelete</span></div>';
                }
              }

              else
              {
                if(star_array[temp_store[i].id]==1)
                {
                  html += '<div style="background-color:gray;" class="notice_info" id="notice_' + temp_store[i].id + '" onclick="open_notice(' + temp_store[i].id + ')">' + '<input type="checkbox" class="check" id="check-' + temp_store[i].id + '" onclick="add_to_checklist(' + temp_store[i].id + ', event)">' + '<span class="read" id=notice_read_' + temp_store[i].id + '></span><span class="starred" onclick="star_notice(' + temp_store[i].id + ', event)">S&nbsp</span>' + temp_store[i].subject + '<span class="edit" onclick="edit_notice(' + temp_store[i].id + ', event)">&nbsp&nbspEdit</span><span class="delete" onclick="delete_notice(' + temp_store[i].id + ', event)">&nbsp&nbspDelete</span></div>';
                }
                else
                {
                  html += '<div class="notice_info" id="notice_' + temp_store[i].id + '" onclick="open_notice(' + temp_store[i].id + ')">' + '<input type="checkbox" class="check" id="check-' + temp_store[i].id + '" onclick="add_to_checklist(' + temp_store[i].id + ', event)">' + '<span class="read" id=notice_read_' + temp_store[i].id + '></span><span class="starred" onclick="star_notice(' + temp_store[i].id + ', event)">S&nbsp</span>' + temp_store[i].subject + '<span class="edit" onclick="edit_notice(' + temp_store[i].id + ', event)">&nbsp&nbspEdit</span><span class="delete" onclick="delete_notice(' + temp_store[i].id + ', event)">&nbsp&nbspDelete</span></div>';
                }
              }
            }
           else
           {
              if(read_array[temp_store[i].id]==1)
              {
                if(star_array[temp_store[i].id]==1)
                {
                  html += '<div style="background-color:gray;" class="notice_info" id="notice_' + temp_store[i].id + '" onclick="open_notice(' + temp_store[i].id + ')">' + '<input type="checkbox" class="check" id="check-' + temp_store[i].id + '" onclick="add_to_checklist(' + temp_store[i].id + ', event)">' + '<span class="read" id=notice_read_' + temp_store[i].id + '>R&nbsp</span><span class="starred" onclick="star_notice(' + temp_store[i].id + ', event)">S&nbsp</span>' + temp_store[i].subject + '</div>';
                }
                else
                {
                  html += '<div class="notice_info" id="notice_' + temp_store[i].id + '" onclick="open_notice(' + temp_store[i].id + ')">' + '<input type="checkbox" class="check" id="check-' + temp_store[i].id + '" onclick="add_to_checklist(' + temp_store[i].id + ', event)">' + '<span class="read" id=notice_read_' + temp_store[i].id + '>R&nbsp</span><span class="starred" onclick="star_notice(' + temp_store[i].id + ', event)">S&nbsp</span>' + temp_store[i].subject + '</div>';
                }
              }

              else
              {
                if(star_array[temp_store[i].id]==1)
                {
                  html += '<div style="background-color:gray;" class="notice_info" id="notice_' + temp_store[i].id + '" onclick="open_notice(' + temp_store[i].id + ')">' + '<input type="checkbox" class="check" id="check-' + temp_store[i].id + '" onclick="add_to_checklist(' + temp_store[i].id + ', event)">' + '<span class="read" id=notice_read_' + temp_store[i].id + '></span><span class="starred" onclick="star_notice(' + temp_store[i].id + ', event)">S&nbsp</span>' + temp_store[i].subject + '</div>';
                }
                else
                {
                  html += '<div class="notice_info" id="notice_' + temp_store[i].id + '" onclick="open_notice(' + temp_store[i].id + ')">' + '<input type="checkbox" class="check" id="check-' + temp_store[i].id + '" onclick="add_to_checklist(' + temp_store[i].id + ', event)">' + '<span class="read" id=notice_read_' + temp_store[i].id + '></span><span class="starred" onclick="star_notice(' + temp_store[i].id + ', event)">S&nbsp</span>' + temp_store[i].subject + '</div>';
                }
              }
           }
        }
      }
      else
      {

        for(var i=a; i<b; i++)
        {
          html += '<div class="notice_info" onclick="open_notice(' + temp_store[i].id + ')">' + temp_store[i].subject + '</div>';
        }
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
      html = '<p>Subject : ' + data.subject + '<br>';
      html += 'Reference : ' + data.reference + '<br>';
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
              list_notices(page_no);
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
           list_notices(page_no);
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
      list_notices(page_no);
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
    url = ">>" + x.toString() + "--" + (x+86400000).toString();
  }
    console.log(url);
  return url
}

function search()
{
        console.log("search_function_enter");
	j=0;url="";
	query1=$("#search_data").val();
  if(query1=="")
    query1=search_string;
  else
  {
    search_string=query1;
  }
  if(check_if_date(query1))
    url=check_if_date(query1);
  else
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
        console.log("done");
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
                    html += '<div style="background-color:gray;" class="notice_info" id="notice_' + search_store[i].id + '" onclick="open_notice(' + search_store[i].id + ')">' + '<input type="checkbox" class="check" id="check-' + search_store[i].id + '" onclick="add_to_checklist(' + search_store[i].id + ', event)">'  + '<span class="read" id="notice_read_' + search_store[i].id + '">R&nbsp</span><span class="starred" onclick="star_notice(' + search_store[i].id + ', event)">S&nbsp</span>' + search_store[i].subject + '<span class="edit" onclick="edit_notice(' + search_store[i].id + ', event)">&nbsp&nbspEdit</span><span class="delete" onclick="delete_notice(' + search_store[i].id + ', event)">&nbsp&nbspDelete</span></div>';
                  }
                  else
                  {
                    html += '<div class="notice_info" id="notice_' + search_store[i].id + '" onclick="open_notice(' + search_store[i].id + ')">'  + '<input type="checkbox" class="check" id="check-' + search_store[i].id + '" onclick="add_to_checklist(' + search_store[i].id + ', event)">' + '<span class="read" id="notice_read_' + search_store[i].id + '">R&nbsp</span><span class="starred" onclick="star_notice(' + search_store[i].id + ', event)">S&nbsp</span>' + search_store[i].subject + '<span class="edit" onclick="edit_notice(' + search_store[i].id + ', event)">&nbsp&nbspEdit</span><span class="delete" onclick="delete_notice(' + search_store[i].id + ', event)">&nbsp&nbspDelete</span></div>';
                  }
                }

                else
                {
                  if(star_array[search_store[i].id]==1)
                  {
                    html += '<div style="background-color:gray;" class="notice_info" id="notice_' + search_store[i].id + '" onclick="open_notice(' + search_store[i].id + ')">'  + '<input type="checkbox" class="check" id="check-' + search_store[i].id + '" onclick="add_to_checklist(' + search_store[i].id + ', event)">' + '<span class="read" id="notice_read_' + search_store[i].id + '"></span><span class="starred" onclick="star_notice(' + search_store[i].id + ', event)">S&nbsp</span>' + search_store[i].subject + '<span class="edit" onclick="edit_notice(' + search_store[i].id + ', event)">&nbsp&nbspEdit</span><span class="delete" onclick="delete_notice(' + search_store[i].id + ', event)">&nbsp&nbspDelete</span></div>';
                  }
                  else
                  {
                    html += '<div class="notice_info" id="notice_' + search_store[i].id + '" onclick="open_notice(' + search_store[i].id + ')">'  + '<input type="checkbox" class="check" id="check-' + search_store[i].id + '" onclick="add_to_checklist(' + search_store[i].id + ', event)">' + '<span class="read" id="notice_read_' + search_store[i].id + '"></span><span class="starred" onclick="star_notice(' + search_store[i].id + ', event)">S&nbsp</span>' + search_store[i].subject + '<span class="edit" onclick="edit_notice(' + search_store[i].id + ', event)">&nbsp&nbspEdit</span><span class="delete" onclick="delete_notice(' + search_store[i].id + ', event)">&nbsp&nbspDelete</span></div>';
                  }
                }
              }
              else
              {
                  if(read_array[search_store[i].id]==1)
                  {
                    if(star_array[search_store[i].id]==1)
                    {
                      html += '<div style="background-color:gray;" class="notice_info" id="notice_' + search_store[i].id + '" onclick="open_notice(' + search_store[i].id + ')">' + '<input type="checkbox" class="check" id="check-' + search_store[i].id + '" onclick="add_to_checklist(' + search_store[i].id + ', event)">'  + '<span class="read" id="notice_read_' + search_store[i].id + '">R&nbsp</span><span class="starred" onclick="star_notice(' + search_store[i].id + ', event)">S&nbsp</span>' + search_store[i].subject + '</div>';
                    }
                    else
                    {
                      html += '<div class="notice_info" id="notice_' + search_store[i].id + '" onclick="open_notice(' + search_store[i].id + ')">'  + '<input type="checkbox" class="check" id="check-' + search_store[i].id + '" onclick="add_to_checklist(' + search_store[i].id + ', event)">' + '<span class="read" id="notice_read_' + search_store[i].id + '">R&nbsp</span><span class="starred" onclick="star_notice(' + search_store[i].id + ', event)">S&nbsp</span>' + search_store[i].subject + '</div>';
                    }
                  }

                  else
                  {
                    if(star_array[search_store[i].id]==1)
                    {
                      html += '<div style="background-color:gray;" class="notice_info" id="notice_' + search_store[i].id + '" onclick="open_notice(' + search_store[i].id + ')">'  + '<input type="checkbox" class="check" id="check-' + search_store[i].id + '" onclick="add_to_checklist(' + search_store[i].id + ', event)">' + '<span class="read" id="notice_read_' + search_store[i].id + '"></span><span class="starred" onclick="star_notice(' + search_store[i].id + ', event)">S&nbsp</span>' + search_store[i].subject + '</div>';
                    }
                    else
                    {
                      html += '<div class="notice_info" id="notice_' + search_store[i].id + '" onclick="open_notice(' + search_store[i].id + ')">'  + '<input type="checkbox" class="check" id="check-' + search_store[i].id + '" onclick="add_to_checklist(' + search_store[i].id + ', event)">' + '<span class="read" id="notice_read_' + search_store[i].id + '"></span><span class="starred" onclick="star_notice(' + search_store[i].id + ', event)">S&nbsp</span>' + search_store[i].subject + '</div>';
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
        			    html += '<div style="background-color:gray;" class="notice_info" id="notice_' + upload_array[i].id + '" onclick="open_notice(' + upload_array[i].id + ')">'  + '<input type="checkbox" class="check" id="check-' + upload_array[i].id + '" onclick="add_to_checklist(' + upload_array[i].id + ', event)">' + '<span class="read" id=notice_read_' + upload_array[i].id + '>R&nbsp</span><span class="starred" onclick="star_notice(' + upload_array[i].id + ', event)">S&nbsp</span>' + upload_array[i].subject + '<span class="edit" onclick="edit_notice(' + upload_array[i].id + ', event)">&nbsp&nbspEdit</span><span class="delete" onclick="delete_notice(' + upload_array[i].id + ', event)">&nbsp&nbspDelete</span></div>';
			        }
			        else
			        {
        			    html += '<div class="notice_info" id="notice_' + upload_array[i].id + '" onclick="open_notice(' + upload_array[i].id + ')">'  + '<input type="checkbox" class="check" id="check-' + upload_array[i].id + '" onclick="add_to_checklist(' + upload_array[i].id + ', event)">' + '<span class="read" id=notice_read_' + upload_array[i].id + '>R&nbsp</span><span class="starred" onclick="star_notice(' + upload_array[i].id + ', event)">S&nbsp</span>' + upload_array[i].subject + '<span class="edit" onclick="edit_notice(' + upload_array[i].id + ', event)">&nbsp&nbspEdit</span><span class="delete" onclick="delete_notice(' + upload_array[i].id + ', event)">&nbsp&nbspDelete</span></div>';
			        }
          }

          else
          {
			        if(star_array[upload_array[i].id]==1)
			        {
        			  html += '<div style="background-color:gray;" class="notice_info" id="notice_' + upload_array[i].id + '" onclick="open_notice(' + upload_array[i].id + ')">'  + '<input type="checkbox" class="check" id="check-' + upload_array[i].id + '" onclick="add_to_checklist(' + upload_array[i].id + ', event)">' + '<span class="read" id=notice_read_' + upload_array[i].id + '></span><span class="starred" onclick="star_notice(' + upload_array[i].id + ', event)">S&nbsp</span>' + upload_array[i].subject + '<span class="edit" onclick="edit_notice(' + upload_array[i].id + ', event)">&nbsp&nbspEdit</span><span class="delete" onclick="delete_notice(' + upload_array[i].id + ', event)">&nbsp&nbspDelete</span></div>';
			        }
			        else
			        {
        			    html += '<div class="notice_info" id="notice_' + upload_array[i].id + '" onclick="open_notice(' + upload_array[i].id + ')">'  + '<input type="checkbox" class="check" id="check-' + upload_array[i].id + '" onclick="add_to_checklist(' + upload_array[i].id + ', event)">' + '<span class="read" id=notice_read_' + upload_array[i].id + '></span><span class="starred" onclick="star_notice(' + upload_array[i].id + ', event)">S&nbsp</span>' + upload_array[i].subject + '<span class="edit" onclick="edit_notice(' + upload_array[i].id + ', event)">&nbsp&nbspEdit</</span><span class="delete" onclick="delete_notice(' + upload_array[i].id + ', event)">&nbsp&nbspDelete</span></div>';
			        }
          }

		}
	}
      html += '</div>';
      $('#content').append(html);
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
    html = '<div id="menu" style="width:130px;height:70px;position:absolute;background-color:rgb(202, 228, 13);margin-top:16px;margin-left:159px;">'
    html += '<div style="margin-top:2px;margin-left:7%;" onclick="read_star_checklist(3)">Mark as read</div>'
    html += '<div style="margin-left:7%;" onclick="read_star_checklist(4)">Mark as unread</div>'
    html += '<div style="margin-left:7%;" onclick="read_star_checklist(1)">Mark as starred</div>'
    html += '<div style="margin-left:7%;" onclick="read_star_checklist(2)">Mark as unstarred</div></div>'
    $('#super_more').append(html);
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
      html = 'Error';
      $('#content').empty();
      $('#content').append(html);
    }
	});
}

function display_categories()
{
  console.log("hello");
  if(select_category==0)
  {
    $("#select_category").css("background-color", "#97968D");
    html = '<div id="category_menu" style="width:860px;height:181px;position:absolute;background-color:rgb(202, 228, 13);">'
    html += '<div id="category_list" style="float:left;">'
    var a = Object.keys(constants);
    for(var i=0;i<5;i++)
      html += '<div style="margin-top:2px;" onclick="change_category_bar_name(\'' + a[i] +'\', \'All\')"  onmouseover="display_sub_categories(\'' + a[i] + '\')">' + a[i] + '</div>';
    html += '</div>'
    html += '<div id="category_details" style="width:650px;float:left;margin-left:15%;">'
    html += '<div id="category_child1" style="float:left;width:290px;"></div>'
    html += '<div id="category_child2" style="float:left;width:290px;"></div>'
    html += '</div></div>'
    $('#category_master_div').append(html);
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
  html='';
  for(var i=0;i<k;i++)
  html += '<div id="' + main_category + '_' + i + '" onclick="change_category_bar_name(\'' + main_category + '\',\'' + constants[main_category][i] + '\')">' + constants[main_category][i] + '</div>'
  $('#category_child1').empty();
  $('#category_child2').empty();
  $('#category_child1').append(html);
  html='';
  var j;
  for(j=k;j<len;j++)
  html += '<div id="' + main_category + '_' + j + '" onclick="change_category_bar_name(\'' + main_category + '\',\'' + constants[main_category][j] + '\')">' + constants[main_category][j] + '</div>'
  if(j!=9)
  $('#category_child2').append(html);
}

function change_category_bar_name(main_category, category)
{
  if(m_category==main_category && sub_category==category)
  {
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
