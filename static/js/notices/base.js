var search_total_pages, search_last_page_notices, search_store;		//variables for search results
var upload_total_pages, upload_last_page_notices, upload_array;		//variables for show_uploads results
var total_pages, last_page_notices;		//variables for general new notice display(all)
var old_total_pages, old_last_page_notices;		//variables for general expired notice display(all)
var temp_total_pages, temp_last_page_notices;		//variables for general notice display(specific category)
var store = new Array(50), temp_store = new Array(50), old_store= new Array(50);    //store stands for new store or the store of new notices.
var emptyarray = new Array(50);

var main_mode="display", sub_mode="", m_category="All", sub_category="All", cur_page_no="1", more, name_to_display, all=1, same_except_page_no=1, search_string="", search_string_changed=0;
var h1,h2,h3,h4,h5;
/*
  1.Values of sub_mode can be either new or old
  2.same_except_page_no stores if everything is same except the page number
  2.same_except_page_no stores if the newly arrived categories(h3, h4) matches with the old ones
  3.Values of main mode can be display, upload, search, content
  4.The all variable stores if the both the m_category and sub_category are equal to "All" or not.
*/

var privelege=0, first_time_visit=0, static_divs_created=0, star_perm=0, select_category=0;
var checklist, check_upload_array={}, star_array={}, read_array={};

/*
    1.star_array stores the ids of notices who are starred for a particular user.read_array is similar
    2.search_store stores the results of a particular search
    3.star_perm is 0 when the app is being used anonymously
*/

function first_time_functions()                 //This function is responsible for calling 6 important basic functions to store necessary data
{
    get_privelege();                            //First time function 1
}

$(document).on("load_app_notices", function(e, hash1, hash2, hash3, hash4, hash5){
    h1=hash1;    //The function redirection can only be called once the first_time_functions have played their part. So, we store the current state variables for now.
    h2=hash2;
    h3=hash3;
    h4=hash4;
    h5=hash5;

    console.log("entered load_app_notices");
    if(first_time_visit==0)
      first_time_functions();
    else
      redirection();
});

function redirection()            //The main controller function which defines the function path, execution will follow
{
    if(h1 == "content")                              //If the main_mode is content, cut the crap and directly display the notice
    {
        main_mode = "content";
        console.log("display content");
        display_notice(parseInt(h2));
    }
    else
    {

        if(h1==main_mode && h2==sub_mode && h3==m_category && h4==sub_category)     //Setting the value of the same_except_page_no variable
          same_except_page_no=1;
        else
        {
          console.log("abcqw");
          same_except_page_no=0;
        }

        if(h1 == undefined || h1 == "")                           //Setting default values to the primary parameters, if they are undefined
        {
          console.log("clicked on 'notices' app");
          h1="display";
          h2="new";
          h3="All";
          h4="All";
          h5="1";
          $("#global_search_bar").val("");
          $("#global_search_bar").attr('placeholder', 'Search In Notices');
          if(static_divs_created==0)
          {
            create_static_divs();
            static_divs_created=1;            //made 1, so that switched_to_notices is not called again, 4 lines later
          }
        }
       
        if(main_mode=="content" && static_divs_created==0)
        {          
            create_static_divs();
        }

        static_divs_created=0;            //made 0, so that switched_to_notices is not called again. Whichever function creates the static divs makes sure that the value of this variable is non-zero, so that the other reasons don't create them again.
        main_mode=h1;                                                //Setting global variables equal to the ones just arrived
        sub_mode=h2;
        m_category=h3;
        sub_category=h4;
        cur_page_no=h5;

        if(m_category=="All"&&sub_category=="All")                          //Setting the value of the all variable
          all=1;
        else
          all=0;

        checklist={};
        more=0;
        if(sub_category=="All")
          $("#select_category").text(m_category);
        else
          $("#select_category").text(sub_category);

      
        if(main_mode=="display")
        {
              if(same_except_page_no==0)
              {
                if(all==1)
                {
                    if(sub_mode=="new")
                    {
                      temp_store=store;
                      temp_total_pages=total_pages;
                      temp_last_page_notices=last_page_notices;
                    }
                    else
                    {
                      temp_store=old_store;
                      temp_total_pages=old_total_pages;
                      temp_last_page_notices=old_last_page_notices;
                    }
      			        load_numbers_bar(temp_total_pages, ""); //loading the numbers bar, since we already know the total pages,last page notices
                    first_time_check();
                    gap_scanner();                            //Checking for gaps. First 50 notices are already present in temp_array
                }
                else
                {
                    console.log("display all!=1 same_except_page_no=0")
                    temp_store = new Array(50);
                    get_total_notices_no();
                    first_time_check();
                    gap_filler_first_time("temp"); //Since temp_store is newly created, it needs to have the first 50 notices. Just call this                                                      function and it'll automatically direct it to gap_scanner() after the first 50 notices                                                        arrive
                }
              }
              else
              {
                  first_time_check();
                  list_notices(parseInt(cur_page_no), temp_store, temp_total_pages, temp_last_page_notices);                                                                                                    //Simply call the list function, if nothing except the page no has changed
              }
        }
        else if(main_mode=="show_uploads")
        {
            if(!same_except_page_no)
              load_numbers_bar(upload_total_pages, "upload_");
            list_notices(1, upload_array, upload_total_pages, upload_last_page_notices);
        }
        else if(main_mode=="search")
        {
            $("#global_search_bar").val("");
            $("#global_search_bar").attr('placeholder', search_string);
            if(same_except_page_no && !search_string_changed)
              list_notices(parseInt(cur_page_no), search_store, search_total_pages, search_last_page_notices);
            else
            {
              search_string_changed = 0;
              bring_search_results();
            }
        }
    }
}

/*3 reasons for creation of static divs:
1) "Notices" app is clicked.
2) Notice Board is opened for the first time.
3) Switching from content main_mode to any other notice board main_mode, by pressing back button.
*/

function create_static_divs()                //Create static buttons like upload, new, old, and additional features, when switched
{
    $("#content").empty();
    $("#right-column").empty();
    $('#content').html(welcome_html());
    if(privelege==1)
      $('#content').append(upload_html());
    $('#content').append(newold_buttons_html());
    if(star_perm==1)
    {
      $('#content').append(additional_features_html());
    }
    if(sub_category=="All")
      $('#content').append(load_cat_bar_html(m_category));
    else
      $('#content').append(load_cat_bar_html(sub_category));
    
    $('#content').append('<div id="page_numbers"></div>')
    $('#content').append('<div id="notice_list"></div>');
    console.log("switched_to_noties_create : static divs created")
}

function get_total_notices_no()       //This function is only meant for general notice display(categories other than All, All)
{
  		  $.ajax({
    		  type: 'get',
    		  url : 'notices/temp_max_notices/' + sub_mode + '/' + m_category + '/' + sub_category,
    		  success: function (data)
    		  {
      			temp_last_page_notices = data.total_notices%10;
      			temp_total_pages = Math.floor(data.total_notices/10) ;
      			if (temp_last_page_notices > 0)
        		  temp_total_pages++;
      			load_numbers_bar(temp_total_pages, "");
          }
        });
}

function first_time_check()                                         /* Check if one clicks for the first time on a bundle*/
{
    var bundle_no = parseInt((parseInt(cur_page_no)-1)/5) + 1;
    var len = (temp_store.length/50);
    for(var i=0; i<(bundle_no-len); i++)
      temp_store.push.apply(temp_store, emptyarray);
}

function gap_scanner()                 // Fills the appropriate gaps with notice objects into the store, between indices
{                                                                           // corresponding to the bundle_no.
    console.log("entered_gap_scanner");
    var bundle_no = parseInt((cur_page_no-1)/5) + 1;
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
            gap_filler(gap_begin, gap_end, temp_store[0].id);
            gap_begin = 0;
            temp=0;
          }
          i++;
    }
    if(!gap_end)
    {
      console.log("no gaps found");
      list_notices(parseInt(cur_page_no), temp_store, temp_total_pages, temp_last_page_notices);
    }
}

function gap_filler(llim, hlim, temp)
{
        $.ajax({
        type: 'get',
        url : 'notices/list_notices/' + sub_mode + '/' + m_category + '/' + sub_category + '/' + llim + '/' + hlim + '/' + temp,
        success: function (data)
        {
            console.log("entered gap_filler");
            for(var i = llim; i<=hlim; i++)
              temp_store[i] = data[i-llim];
            if(sub_mode=="new")
              store = temp_store;
            else
              old_store = temp_store;
            list_notices(parseInt(cur_page_no), temp_store, temp_total_pages, temp_last_page_notices);
        },
      });
}

function load_numbers_bar(tp, mode1)        //tp = total pages, mode1 = new, old, search, upload
{
      $('div#page_numbers').empty();
      $('div#page_numbers').append(load_numbers_bar_html(tp, mode1));
      if(mode1=="")
        first_time_check();
}

function change_page(number)
{
  location.hash = '#notices/display/' + sub_mode +'/' +  m_category + '/' +  sub_category + '/' + number;
}

function open_notice(id)
{
  location.hash = '#notices/content/' + id;
}

function upload_change_page(page_no)
{
  location.hash = '#notices/show_uploads/new/All/All/' + page_no;
}

function search_change_page(page_no)
{
  url_temp = '#notices/search/' + sub_mode + '/' + m_category + '/' + sub_category + '/' + page_no;
  if(location.hash == url_temp)
  {
  	hashtags = ["search", sub_mode, m_category, sub_category, String(page_no)];
  	$(document).trigger("load_app_notices", hashtags);
  }
  else
  {
	  location.hash=url_temp;
  }
}

function list_notices(page_no, tstore, ttotal_pages, tlast_page_notices)    //t here stands for temp, representing the local variables
{
      console.log("entered list_notices : " + page_no);
      $('div#notice_list').empty();
      var k = 0;
      if(page_no < ttotal_pages || (page_no == ttotal_pages && tlast_page_notices==0))
        k = 10;
      else
        k = tlast_page_notices;
      var a=(page_no-1)*10, b=a+k;
      context = {};
      for(var i=a; i<b; i++)
      {
            context["notice"] = tstore[i];

            if(star_perm==1)
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

            $('#notice_list').append(list_notices_html(context));

      }
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

function set_search_string()
{
      console.log("entered search");
      if($("#global_search_bar").val()!=search_string)
        search_string_changed=1;
      search_string = $("#global_search_bar").val();
/*      if(search_bar_value=="")
      {
        search_bar_value=search_string;
      }
*/
      search_change_page(1);
}

function check_if_date()
{
      console.log("entered check_if_date")
      url=""
      if(search_string.split("-").length==2)
      {
        parts=search_string.split("-");
        parts[0]=Date.parse(parts[0]);
        parts[1]=Date.parse(parts[1]);
        if(parts[0]>1262284200000 && parts[1]>1262284200000)
        url = ">>" + parts.join().replace(",", "-");
      }
      else if(!isNaN(Date.parse(search_string)) && Date.parse(search_string)>1262284200000)
      {
        x = Date.parse(search_string)
        url = ">>" + x.toString() + "-" + (x+86400000).toString();
      }
      console.log(url);
      return url
}
function bring_search_url()
{
      url = check_if_date();
      if(url=="")
      {
          if(search_string=="")
            return ""
          query=search_string.split(" ");
          t=0;
          k=query.length;
          for(var i=0; i<k;i++)
          {
            if(query[t]=="")
              query.splice(t,1);
            else
              t++;
          }
          for(var i=0; i<query.length-1; i++)
          {
            url+=query[i]+"+";
          }
          url+=query[query.length-1];
      }
      return url;
}

function bring_search_results()
{
      url = bring_search_url();
      console.log(url);
      $.ajax({
          type: 'get',
          url : 'notices/search/' + sub_mode + '/' + m_category + '/' + sub_category + '/?q=' + url,
          success: function (data)
          {
            len=Object.keys(data).length;
            search_total_pages=Math.floor(len/10);
            search_last_page_notices=len%10;
            if(search_last_page_notices>0)
              search_total_pages++;
            search_store = new Array(len);
            search_store = data;
            console.log("search_done");
            console.log(search_store);
            console.log("search_ends");
            load_numbers_bar(search_total_pages, "search_");
            list_notices(parseInt(cur_page_no), search_store, search_total_pages, search_last_page_notices);
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
    if(parseInt(cur_page_no)<temp_total_pages||temp_last_page_notices==0)
      k=10;
    else
    {
      if(main_mode=="display")
          k=temp_last_page_notices;
      else if(main_mode=="show_uploads")
          k=upload_last_page_notices;
      else if(main_mode=="search")
          k=search_last_page_notices;
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
    console.log("entered read_star_checklist t :" + t);
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
    console.log("entered change_category_bar_name")
    $("#select_category").css("background-color", "white");
    $('#category_menu').remove();
    select_category=0;
    if(m_category==main_category && sub_category==category)
      return;
    select_category=0;
    url_temp = '#notices/' + main_mode + '/' + sub_mode + '/' + main_category +'/' +  category + '/1';
    location.hash = url_temp;
}

function newold_clicked(ns)       //ns stands for new status, storing the sub_mode of the button that is clicked.
{
    console.log("entered newold_clicked");
    if(sub_mode!=ns)
    {
      url_temp = '#notices/' + main_mode + '/' + ns + '/' + m_category +'/' +  sub_category + '/1';
      location.hash = url_temp;
    }
}
//Following are the functions that are called the first time, notices is clicked

function get_privelege()
{
		$.ajax({
    		type: 'get',
    		url : 'notices/privelege/',
    		success: function (data)
    		{
			      star_perm=1;
      			if(data.privelege)
      			{
				      privelege=1;
              bring_uploads();                         //First time function 2, in case user is an uploader
      			}
            else
              bring_starred_notices();                   //First time function 2, in case user is logged in and not an uploader
            console.log("loaded get_privelge : privelege: " + privelege + " star_perm : " + star_perm)
    		},
        error: function (data)
        {
            get_total_notices_no_first_time();          //First time function 2, in case of anonymous user
            console.log("loaded get_privelge : anonymous")
        }
  });
}

function get_total_notices_no_first_time()
{
  		  $.ajax({
    		  type: 'get',
    		  url : 'notices/max_notices/',
    		  success: function (data)
    		  {
      			  last_page_notices = data['total_new_notices']%10;
      			  total_pages = Math.floor(data['total_new_notices']/10) ;
      			  if (last_page_notices > 0)
        		    total_pages++;
              old_last_page_notices = data['total_old_notices']%10;
      			  old_total_pages = Math.floor(data['total_old_notices']/10) ;
              if (old_last_page_notices > 0)
        		    old_total_pages++;
              console.log("loaded : total_notices_no old and new");
              gap_filler_first_time("new");
          }
          });
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
    console.log("loaded : starred_notices");
    bring_read_notices();                 //First time function 4, in case user is an uploader
                                          //First time function 3, in case user is logged in and not an uploader
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
    console.log("loaded : read_notices");
    get_total_notices_no_first_time();      //First time function 5, in case user is an uploader
                                        // and function 4, in case user is logged in and not an uploader
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
		    upload_total_pages=Math.floor(len/10);
        upload_last_page_notices=len%10;
        if(upload_last_page_notices>0)
        upload_total_pages++;
        upload_array = new Array(len);
        for(var i=0;i<len;i++)
        {
          upload_array[i] = data[i];
          check_upload_array[data[i].id]=1;
        }
        console.log("loaded : bring_uploads");
        bring_starred_notices();              //First time function 3, in case user is an uploader
      }
   });
}

function gap_filler_first_time(bring_what)
{

        if(bring_what=="new")
          url = 'notices/list_notices/new/All/All/0/49/0';
        else if(bring_what=="old")
          url = 'notices/list_notices/old/All/All/0/49/0';
        else
          url = 'notices/list_notices/' + sub_mode + '/' + m_category + '/' + sub_category + '/0/49/0';

        $.ajax({
        type: 'get',
        url : url,
        success: function (data)
        {
           for(var i = 0; i<=49; i++)
           {
                if(bring_what=="new")
                  store[i] = data[i];
                else if(bring_what=="old")
                  old_store[i] = data[i];
                else if(bring_what=="temp")
                {
                  temp_store[i] = data[i];
                }
           }
           console.log("loaded : gap_filler_first_time : " + bring_what);

           if(bring_what=="temp")
              gap_scanner();          //If the mode is temp, go to normal gap_filler(specially made for this purpose) and scan again for gaps.
           if(bring_what=="new")
              gap_filler_first_time("old");             //First time function 6, in case user is an uploader
                                                        //First time function 5, in case user is logged in and not an uploader
                                                        //First time function 3, in case user is anonymous
           if(bring_what=="old")
           { 
             if(h1!="content")
             {
               create_static_divs();
               static_divs_created=1;
             }
             first_time_visit=1;
             redirection();
           }
        }
        });
}
 
//Following are the functions which bring html from .hbs files

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
}
